import os
from services.markdown_service import MarkdownService, DetailedViewParser

class MarkdownController:
    """Controller for markdown generation functionality."""
    
    def __init__(self, md_view, opts_view, file_types_view, thread_mgr, app):
        self.md_view = md_view
        self.opts_view = opts_view
        self.file_types_view = file_types_view
        self.thread_mgr = thread_mgr
        self.app = app
        self._connect_signals()

    def _connect_signals(self):
        # Connect options changed signal
        self.opts_view.options_changed.connect(self.refresh)

    def refresh(self):
        # Refresh markdown content
        path = self.app.project_explorer_frame.get_selected_path()
        if not path:
            return
            
        if os.path.isfile(path):
            self.refresh_single_file(path)
            return
            
        project_name = os.path.basename(path)
        opts = self.opts_view.get_options()
        remove_imports = opts['remove_imports']
        remove_comments = opts['remove_comments']
        selected_extensions = self.file_types_view.get_selected_extensions()
        excluded_items = self.app.get_excluded_items()

        service = MarkdownService(
            path,
            project_name,
            remove_imports,
            remove_comments,
            selected_extensions,
            excluded_items
        )
        service.markdown_generated.connect(self.on_markdown_generated)
        self.thread_mgr.start_thread(service)

    def refresh_single_file(self, file_path):
        # Process single file and display markdown
        if not os.path.isfile(file_path):
            return
            
        dir_path = os.path.dirname(file_path)
        project_name = os.path.basename(dir_path)
        relative_path = os.path.basename(file_path)
        
        opts = self.opts_view.get_options()
        remove_imports = opts['remove_imports']
        remove_comments = opts['remove_comments']
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read().replace('\r\n', '\n').replace('\r', '\n').strip()
                
            _, extension = os.path.splitext(file_path)
            language = MarkdownService.get_language_by_extension(extension)
            
            if remove_imports and language == "java":
                code = MarkdownService.remove_java_imports(code)
                
            if remove_comments:
                if extension == ".py":
                    from services.markdown_service import remove_python_comments
                    code = remove_python_comments(code)
                elif extension in C_LIKE_EXTENSIONS:
                    code = MarkdownService.remove_c_like_comments(code)
                    
            header = f"**{project_name}/{relative_path}**"
            markdown = "\n".join([header, f"```{language}", code, "```"])
            
            self.on_markdown_generated(markdown)
            
        except Exception as e:
            error_message = f"**Error processing {file_path}:**\n```\n{str(e)}\n```"
            self.on_markdown_generated(error_message)

    def on_markdown_generated(self, markdown):
        # Handle generated markdown content
        self.md_view.update_content(markdown)