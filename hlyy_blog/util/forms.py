class FormMixin:
    def get_error(self):
        # 将表单验证的错误信息构造得更可读
        new_errors = {}
        if hasattr(self, 'errors'):
            errors = self.errors.get_json_data()
            for key, message_dicts in errors.items():
                messages = []
                for message in message_dicts:
                    messages.append(message['message'])
                new_errors[key] = messages
        return new_errors