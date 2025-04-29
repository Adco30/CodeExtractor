import ast
import fnmatch
import os
import time
import re
from typing import List

import javalang
from PyQt5.QtCore import QThread, pyqtSignal

from constants import C_LIKE_EXTENSIONS

class DetailedViewParser:
    """Parser for detailed file structure views."""
    
    @staticmethod
    def parse_file(file_path):
        # Parse file based on extension
        _, ext = os.path.splitext(file_path)
        if ext == '.py':
            return DetailedViewParser.parse_python_file(file_path)
        elif ext == '.java':
            return DetailedViewParser.parse_java_file(file_path)
        elif ext == '.swift':
            return DetailedViewParser.parse_swift_file(file_path)
        return []

    @staticmethod
    def parse_python_file(file_path):
        # Parse Python file structure
        try:
            with open(file_path, 'r') as file:
                tree = ast.parse(file.read())

            details = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    details.append(f"class {node.name}:")
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            args = [arg.arg for arg in item.args.args]
                            args_str = ', '.join(args)
                            details.append(f"    def {item.name}({args_str})")
                elif isinstance(node, ast.FunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    args_str = ', '.join(args)
                    details.append(f"def {node.name}({args_str})")
            return details
        except Exception as e:
            print(f"Error parsing Python file {file_path}: {str(e)}")
            return []

    @staticmethod
    def parse_java_file(file_path):
        # Parse Java file structure
        try:
            with open(file_path, 'r') as file:
                tree = javalang.parse.parse(file.read())

            details = []
            for path, node in tree.filter(javalang.tree.ClassDeclaration):
                details.append(f"class {node.name}")
                for method in node.methods:
                    params = [f"{param.type.name} {param.name}" for param in method.parameters]
                    params_str = ', '.join(params)
                    return_type = method.return_type.name if method.return_type else 'void'
                    details.append(f"    {return_type} {method.name}({params_str})")
            return details
        except Exception as e:
            print(f"Error parsing Java file {file_path}: {str(e)}")
            return []

    @staticmethod
    def parse_swift_file(file_path):
        # Parse Swift file structure
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            class SwiftEntity:
                def __init__(self, name, kind, signature=""):
                    self.name = name
                    self.kind = kind
                    self.signature = signature
                    self.children = []

                def to_lines(self, indent_level=0):
                    indent_str = "    " * indent_level
                    lines = [f"{indent_str}{self.signature}"]
                    for child in self.children:
                        lines.extend(child.to_lines(indent_level + 1))
                    return lines

            class SwiftMember:
                def __init__(self, signature, kind="member"):
                    self.signature = signature
                    self.kind = kind

                def to_lines(self, indent_level=0):
                    indent_str = "    " * indent_level
                    return [f"{indent_str}{self.signature}"]

            root_entity = SwiftEntity("Root", "root", "Swift File")
            entity_stack = [root_entity]

            entity_pattern = re.compile(
                r'^\s*(?:public|private|internal|open)?\s*(final)?\s*(class|struct|enum)\s+(\w+)(.*)?\{?\s*$'
            )
            func_pattern = re.compile(
                r'^\s*(?:public|private|internal|open)?\s*func\s+(\w+)\s*\(([^)]*)\)\s*(->\s*([A-Za-z0-9_\[\]:<>? ]+))?'
            )
            varlet_pattern = re.compile(
                r'^\s*(?:public|private|internal|open)?\s*(var|let)\s+(\w+)\s*:\s*([^=]+)(=\s*.*)?'
            )
            enum_case_pattern = re.compile(
                r'^\s*case\s+(.+)'
            )

            brace_depth = 0

            for line in lines:
                line = re.sub(r'//.*', '', line)
                line = re.sub(r'/\*.*?\*/', '', line)

                open_braces = line.count('{')
                close_braces = line.count('}')

                match_entity = entity_pattern.match(line)
                if match_entity:
                    final_kw = match_entity.group(1) or ""
                    kind = match_entity.group(2)
                    name = match_entity.group(3)
                    tail = match_entity.group(4) or ""
                    tail = tail.strip()

                    signature = f"{kind} {name}"
                    if tail.startswith(":"):
                        signature += f"{tail}"

                    if final_kw:
                        signature = f"{final_kw} {signature}".strip()

                    new_entity = SwiftEntity(name, kind, signature)
                    entity_stack[-1].children.append(new_entity)
                    entity_stack.append(new_entity)

                else:
                    match_func = func_pattern.match(line)
                    if match_func:
                        func_name = match_func.group(1)
                        params = match_func.group(2).strip()
                        return_type = match_func.group(4) if match_func.group(4) else "Void"
                        signature = f"func {func_name}({params}) -> {return_type}"
                        entity_stack[-1].children.append(SwiftMember(signature, kind="func"))
                    else:
                        match_var = varlet_pattern.match(line)
                        if match_var:
                            varlet = match_var.group(1)
                            var_name = match_var.group(2)
                            var_type = match_var.group(3).strip()
                            signature = f"{varlet} {var_name}: {var_type}"
                            entity_stack[-1].children.append(SwiftMember(signature, kind=varlet))
                        else:
                            match_case = enum_case_pattern.match(line)
                            if match_case and entity_stack[-1].kind == "enum":
                                cases_str = match_case.group(1).strip()
                                cases_split = [c.strip() for c in cases_str.split(',')]
                                for c in cases_split:
                                    entity_stack[-1].children.append(SwiftMember(f"case {c}", kind="case"))

                brace_depth_before = brace_depth
                brace_depth += open_braces
                brace_depth -= close_braces

                while len(entity_stack) > 1 and brace_depth < brace_depth_before:
                    entity_stack.pop()
                    brace_depth_before -= 1

            return root_entity.to_lines(0)[1:]
        except Exception as e:
            print(f"Error parsing Swift file {file_path}: {str(e)}")
            return []

def remove_python_comments(code):
    lines = code.split('\n')
    filtered_lines = []
    in_block_comment = False
    consecutive_empty = 0
    for line in lines:
        stripped = line.strip()
        if not in_block_comment:
            if '"""' in line or "'''" in line:
                comment_delimiter = '"""' if '"""' in line else "'''"
                start_idx = line.find(comment_delimiter)
                if line.count(comment_delimiter) == 1:
                    line = line[:start_idx].rstrip()
                    in_block_comment = True
                else:
                    end_idx = line.find(comment_delimiter, start_idx + len(comment_delimiter))
                    line = line[:start_idx] + line[end_idx+len(comment_delimiter):]
            if '#' in line:
                line = line.split('#')[0].rstrip()
            if not stripped:
                consecutive_empty += 1
            else:
                consecutive_empty = 0
            if consecutive_empty <= 1:
                filtered_lines.append(line)
        else:
            if '"""' in line or "'''" in line:
                comment_delimiter = '"""' if '"""' in line else "'''"
                end_idx = line.find(comment_delimiter) + len(comment_delimiter)
                in_block_comment = False
                line = line[end_idx:].lstrip()
                if line:
                    filtered_lines.append(line)
    return "\n".join(filtered_lines)

class MarkdownService(QThread):
    """Service for generating markdown from source files."""
    
    markdown_generated = pyqtSignal(str)
    progress_updated = pyqtSignal(int)

    def __init__(self, path, project_name, remove_imports, remove_comments, selected_file_types, excluded_items):
        # Initialize markdown service thread
        super().__init__()
        self.path = path
        self.project_name = project_name
        self.remove_imports = remove_imports
        self.remove_comments = remove_comments
        self.selected_file_types = selected_file_types
        self.excluded_items = excluded_items
        self.interrupted = False
        self.max_processing_time = 10
        self.chunk_size = 50

    def run(self):
        # Run markdown generation process
        start_time = time.time()
        output = []
        file_list = self.get_file_list()
        for i in range(0, len(file_list), self.chunk_size):
            if self.interrupted or (time.time() - start_time) > self.max_processing_time:
                break
            chunk = file_list[i:i + self.chunk_size]
            output.extend(self.process_chunk(chunk))
            progress = min(100, int((i + self.chunk_size) / len(file_list) * 100))
            self.progress_updated.emit(progress)
        if not self.interrupted:
            self.markdown_generated.emit("\n\n".join(output))

    def interrupt(self):
        # Interrupt processing
        self.interrupted = True

    def get_file_list(self):
        # Get list of files to process
        file_list = []
        excluded_dirs = [item for item in self.excluded_items if '*' not in item and '.' not in item]
        excluded_files = [item for item in self.excluded_items if '*' in item or '.' in item]
        for root, dirs, files in os.walk(self.path):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in files:
                if any(fnmatch.fnmatch(file, pattern) for pattern in excluded_files):
                    continue
                file_path = os.path.join(root, file)
                _, extension = os.path.splitext(file)
                if self.selected_file_types is not None and extension not in self.selected_file_types:
                    continue
                file_list.append(file_path)
        return file_list

    def process_chunk(self, chunk):
        # Process chunk of files
        output = []
        for file_path in chunk:
            if self.interrupted:
                break
            relative_path = os.path.relpath(file_path, self.path)
            _, extension = os.path.splitext(file_path)
            if self.is_text_file(file_path):
                language = self.get_language_by_extension(extension)
                header = f"**{self.project_name}/{relative_path}**"
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        code = f.read().replace('\r\n', '\n').replace('\r', '\n').strip()
                    if self.remove_imports and language == "java":
                        code = self.remove_java_imports(code)
                    if self.remove_comments:
                        if extension == ".py":
                            code = remove_python_comments(code)
                        elif extension in C_LIKE_EXTENSIONS:
                            code = self.remove_c_like_comments(code)
                    section = "\n".join([header, f"```{language}", code, "```"])
                    output.append(section)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        return output

    @staticmethod
    def is_text_file(file_path):
        # Check if file is text file
        try:
            with open(file_path, "r") as f:
                f.read()
            return True
        except (UnicodeDecodeError, IOError):
            return False

    @staticmethod
    def get_language_by_extension(extension):
        # Get language from file extension
        language_map = {
            ".java": "java", ".py": "python", ".swift": "swift",
            ".c": "c", ".cpp": "cpp", ".h": "c", ".hpp": "cpp",
            ".html": "html", ".js": "javascript", ".xml": "xml",
            ".properties": "properties", ".yml": "yaml", ".yaml": "yaml",
            ".kt": "kotlin", ".kts": "kotlin", ".cs": "csharp",
            ".go": "go", ".php": "php"
        }
        return language_map.get(extension, "")

    @staticmethod
    def remove_java_imports(code):
        # Remove Java import statements
        lines = code.split("\n")
        return "\n".join([line for line in lines if not line.strip().startswith("import ")])

    @staticmethod
    def remove_c_like_comments(code):
        # Remove C-style comments
        code = re.sub(r'//.*?$', '', code, flags=re.MULTILINE)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        return code

class ThreadManager:
    """Manager for thread operations."""
    
    def __init__(self):
        # Initialize thread manager
        self.current_thread = None

    def start_thread(self, thread):
        # Start new thread
        if self.current_thread and self.current_thread.isRunning():
            self.current_thread.interrupt()
        self.current_thread = thread
        self.current_thread.start()

    def interrupt_current(self):
        # Interrupt current thread
        if self.current_thread and self.current_thread.isRunning():
            self.current_thread.interrupt()