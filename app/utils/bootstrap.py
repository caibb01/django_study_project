from django import forms


class BootStrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # 继承父类__init__的方法
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加"class": "form-control",
        for name, field in self.fields.items():
            if name == "create_time":
                field.widget.attrs = {
                    "class": "input-group date form-control  ",

                }
                continue
            #     continue # 这里可以设置指定字段的样式
            # print(name, field)  # 查看返回的内容是什么
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
