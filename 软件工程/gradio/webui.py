import gradio as gr
import pandas as pd

all_lessons = pd.DataFrame({
    "选定": ["〇是 〇否", "〇是 〇否", "〇是 〇否", "〇是 〇否", "〇是 〇否", "〇是 〇否", "〇是 〇否"],
    "课程名称": ["可选选题1", "可选选题2", "可选选题3", "可选选题4", "可选选题5", "可选选题6", "可选选题7"],
    "课程编号": ["20240001", "20240002", "20240003", "20240004", "20240005", "20240006", "20240007"],
    "开课学院": ["计算机学院", "电子工程学院", "通信工程学院", "自动化学院", "计算机学院", "电子工程学院", "通信工程学院"],
    "指导教师": ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九"],
    "剩余名额": [10, 10, 10, 10, 10, 10, 10],
    "已选人数": [0, 0, 0, 0, 0, 0, 0],
})

my_lessons = pd.DataFrame({
    "选定": ["〇是 〇否", "〇是 〇否"],
    "课程名称": ["已选选题1", "已选选题2"],
    "课程编号": ["20240001", "20240002"],
    "开课学院": ["计算机学院", "电子工程学院"],
    "指导教师": ["张三", "李四"],
    "审批结果": ["已通过", "未通过"]
})

student_info = pd.DataFrame({
    "学号": ["B22080415", "B22080416", "B22080417", "B22080418", "B22080419", "B22080420", "B22080421"],
    "姓名": ["吴文韬", "李四", "王五", "赵六", "钱七", "孙八", "周九"],
    "性别": ["男", "女", "男", "女", "男", "女", "男"],
    "年龄": [20, 20, 20, 20, 20, 20, 20],
    "联系方式": ["12345678901", "12345678902", "12345678903", "12345678904", "12345678905", "12345678906", "12345678907"],
    "年级": ["2022", "2022", "2022", "2022", "2022", "2022", "2022"],
    "所在院系": ["物联网学院", "电子工程学院", "通信工程学院", "自动化学院", "物联网学院", "电子工程学院", "通信工程学院"],
    "专业名称": ["网络工程", "电子信息工程", "通信工程", "自动化", "网络工程", "电子信息工程", "通信工程"],
    "选题名称": ["选题1", "选题2", "未选题", "未选题", "未选题", "选题6", "选题7"],
    "指导教师": ["张三", "李四", "未选题", "未选题", "未选题", "孙八", "周九"],
})

teacher_info = pd.DataFrame({
    "工号": ["T20240101", "T20240102", "T20240103", "T20240104", "T20240105", "T20240106", "T20240107"],
    "姓名": ["教师一", "教师二", "教师三", "教师四", "教师五", "教师六", "教师七"],
    "性别": ["男", "女", "男", "女", "男", "女", "男"],
    "年龄": [40, 40, 40, 40, 40, 40, 40],
    "联系方式": ["12345678901", "12345678902", "12345678903", "12345678904", "12345678905", "12345678906", "12345678907"],
    "所属院系": ["物联网学院", "电子工程学院", "通信工程学院", "自动化学院", "物联网学院", "电子工程学院", "通信工程学院"],
    "职称": ["教授", "副教授", "讲师", "教授", "副教授", "讲师", "教授"],
    "负责选题": ["选题1,选题2", "无", "选题3,选题4", "无", "选题5", "选题6", "无"],
})

def student():
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 学生基本信息")
            gr.Textbox(label="学号", value="B22080415", interactive=True)
            gr.Textbox(label="姓名", value="吴文韬", interactive=True)
            gr.Textbox(label="性别", value="男", interactive=True)
            gr.Textbox(label="年龄", value="20", interactive=True)
            gr.Textbox(label="联系方式", value="12345678901", interactive=True)
            gr.Dropdown(label="年级", choices=["2022", "2021", "2020", "2019"], interactive=True)
            gr.Dropdown(label="所在院系", choices=["物联网学院", "电子工程学院", "通信工程学院", "自动化学院"],interactive=True)
            gr.Dropdown(label="专业名称", choices=["网络工程", "电子信息工程", "通信工程", "自动化"], interactive=True)
            gr.Button(value="修改基本信息", interactive=True, variant="primary")
        with gr.Column(scale=3):
            gr.Markdown("### 选题信息")
            with gr.Tabs():
                with gr.TabItem(label="查询所有选题"):
                    gr.Textbox(label="查找选题", placeholder="请输入选题名, 编号或指导教师名字", interactive=True, scale=3)
                    gr.Button(value="查找", scale=1)
                    gr.Markdown("### 所有选题")
                    gr.DataFrame(all_lessons, interactive=False)
                    gr.TextArea(label="自我介绍，能力介绍",interactive=True)
                    gr.Button(value="选择所选选题", interactive=True, variant="primary")
                    gr.Textbox(label="输出信息", value="请先选择选题", interactive=False)
                with gr.TabItem(label="我的选题"):
                    gr.Markdown("### 已选选题")
                    gr.DataFrame(my_lessons, interactive=False)
                    gr.Button(value="取消选择", interactive=True, variant="primary")
                    gr.Textbox(label="输出信息", value="请先选择选题", interactive=False)
                with gr.TabItem(label="选题介绍"):
                    gr.Dropdown(label="选择选题", choices=["选题1", "选题2", "选题3"], interactive=True)
                    gr.Button(value="查看选题详情", interactive=True, variant="primary")
                    gr.TextArea(label="选题详情", 
                                value="""选题详情\n选题名称：选题1\n指导教师：张三，计算机学院教授。联系方式：12345678901\n选题简介：选题1是关于计算机科学与技术的研究，主要研究计算机硬件和软件的优化，以提高计算机的性能和效率。\n总名额：10，已选人数：0，剩余名额：10\n需要学生具备以下能力：熟练掌握计算机基础知识，具备一定的编程能力。掌握至少一种编程语言，如C、C++、Java等。会简单的使用Linux系统，熟悉常用的开发工具，如VSCode、PyCharm等。""", 
                                interactive=False)
                    gr.TextArea(label="指导教师详情", 
                                value="""指导教师详情\n指导教师：张三\n指导教师简介：张三，计算机学院教授。主要研究方向为计算机硬件和软件的优化，以提高计算机的性能和效率。已指导多名学生完成毕业设计（论文）。\n联系方式：12345678901\n办公地点：计算机学院教学楼A座101室""", 
                                interactive=False)

def teacher():
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 教师基本信息")
            gr.Textbox(label="工号", value="T20240101", interactive=True)
            gr.Textbox(label="姓名", value="教师一", interactive=True)
            gr.Textbox(label="性别", value="男", interactive=True)
            gr.Textbox(label="年龄", value="35", interactive=True)
            gr.Textbox(label="联系方式", value="12345678901", interactive=True)
            gr.Textbox(label="邮箱", value="12345678901@njupt.edu.cn", interactive=True)
            gr.Dropdown(label="所属院系", choices=["物联网学院", "电子工程学院", "通信工程学院", "自动化学院"],interactive=True)
            gr.Dropdown(label="职称", choices=["教授", "副教授", "讲师"], interactive=True)
            gr.Button(value="修改基本信息", interactive=True, variant="primary")
        with gr.Column(scale=3):
            gr.Markdown("### 管理选题")
            with gr.Tabs():
                with gr.TabItem(label="发布选题"):
                    gr.Markdown("请输入需要发布的选题信息，包括选题名称、选题简介、总名额、需要学生具备的能力。课程编号无需手动输入，系统将自动生成。选题发布后，学生可查看并选择该选题。")
                    gr.Textbox(label="选题名称", placeholder="请输入选题名称", interactive=True)
                    gr.TextArea(label="选题简介", 
                                value="选题简介：请输入选题简介\n总名额：请输入总名额\n需要学生具备的能力：请输入学生需要具备的能力", 
                                interactive=True)
                    gr.Button(value="发布选题", interactive=True, variant="primary")
                    gr.Textbox(label="输出信息", value="请先发布选题", interactive=False)
                with gr.TabItem(label="修改选题"):
                    gr.Dropdown(label="选择需要修改选题", choices=["选题1", "选题2", "选题3"], interactive=True)
                    gr.Textbox(label="修改选题名称", placeholder="请输入选题名称", interactive=True)
                    gr.TextArea(label="修改选题简介",
                                value="选题简介：请输入选题简介\n总名额：请输入总名额\n需要学生具备的能力：请输入学生需要具备的能力", 
                                interactive=True)
                    gr.Checkbox(label="删除选题", interactive=True)
                    gr.Button(value="确认修改选题", interactive=True, variant="primary")
                    gr.Textbox(label="输出信息", value="请先选择选题", interactive=False)
                with gr.TabItem(label="审批学生选题"):
                    gr.Markdown("此页面用于审核学生提交的选题信息，包括学生基本信息、选题信息。老师可选择同意或拒绝学生的选题申请。选择完成后，系统将自动发送通知给学生，并且学生可在选题页面查看审批结果。<br>选择同意或拒绝学生的选题申请，将自动跳转至下一个需要审批的学生，直到所有学生的选题申请都被审批。")
                    gr.TextArea(label="学生选题信息", 
                                value="学号：B22080415\n姓名：吴文韬\n选题名称：选题1\n指导教师：张三\n联系方式：12345678901\n自我介绍，能力介绍：此处显示学生所填写的内容", 
                                interactive=False)
                    with gr.Row():
                        gr.Button(value="同意", interactive=True, variant="primary")
                        gr.Button(value="拒绝", interactive=True, variant="primary")
                    gr.Textbox(label="输出信息", value="输出信息", interactive=False)
                with gr.TabItem(label="查看学生选择情况"):
                    gr.Dropdown(label="选择选题", choices=["选题1", "选题2", "选题3"], interactive=True)
                    gr.Button(value="查看学生选择情况", interactive=True, variant="primary")
                    gr.TextArea(label="输出信息", 
                                value="已选学生：\n\t学号：B22080415，姓名：吴文韬\n\t学号：B22080416，姓名：李四\n\t学号：B22080417，姓名：王五\n已选人数：3，剩余名额：7", 
                                interactive=False)

def admin():
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 管理员基本信息")
            gr.Textbox(label="工号", value="A20240001", interactive=True)
            gr.Textbox(label="姓名", value="管理员一", interactive=True)
            gr.Textbox(label="性别", value="男", interactive=True)
            gr.Textbox(label="年龄", value="40", interactive=True)
            gr.Textbox(label="联系方式", value="12345678901", interactive=True)
            gr.Textbox(label="邮箱", value="admin@njupt.edu.cn", interactive=True)
            gr.Button(value="修改基本信息", interactive=True, variant="primary")
        with gr.Column(scale=3):
            gr.Markdown("### 管理系统")
            with gr.Tabs():
                with gr.TabItem(label="导入信息"):
                    gr.Markdown("此页面用于导入学生和教师的信息，包括学生基本信息、教师基本信息。导入信息后，系统将自动更新学生和教师的信息。")
                    with gr.Row():
                        gr.File(label="导入或追加学生信息，请选择csv文件或xlsx文件", interactive=True)
                        gr.File(label="导入或追加教师信息，请选择csv文件或xlsx文件", interactive=True)
                    gr.Button(value="导入信息", interactive=True, variant="primary")
                    gr.Textbox(label="输出信息", value="请先导入信息", interactive=False)
                with gr.TabItem(label="查看学生/教师/选题信息"):
                    gr.Markdown("此页面用于查看学生和教师的信息，包括学生基本信息、教师基本信息。")
                    with gr.Tabs():
                        with gr.TabItem(label="查看学生信息"):
                            gr.Textbox(label="查找学生", placeholder="请输入学号或姓名", interactive=True, scale=3)
                            gr.Button(value="查找", scale=1)
                            gr.DataFrame(student_info, interactive=False)
                        with gr.TabItem(label="查看教师信息"):
                            gr.Textbox(label="查找教师", placeholder="请输入工号或姓名", interactive=True, scale=3)
                            gr.Button(value="查找", scale=1)
                            gr.DataFrame(teacher_info, interactive=False)
                        with gr.TabItem(label="查看选题信息"):
                            gr.Textbox(label="查找选题", placeholder="请输入选题编号或选题名称", interactive=True, scale=3)
                            gr.Button(value="查找", scale=1)
                            gr.DataFrame(all_lessons, interactive=False)
                with gr.TabItem(label="删除信息"):
                    gr.Markdown("此页面用于删除学生/教师/选题的信息。")
                    gr.Dropdown(label="选择删除学生", choices=["学生一", "学生二", "学生三"], interactive=True)
                    gr.Button(value="确认删除", interactive=True, variant="primary")
                    gr.Dropdown(label="选择删除教师", choices=["教师一", "教师二", "教师三"], interactive=True)
                    gr.Button(value="确认删除", interactive=True, variant="primary")
                    gr.Dropdown(label="选择删除选题", choices=["选题一", "选题二", "选题三"], interactive=True)
                    gr.Button(value="确认删除", interactive=True, variant="primary")
                    gr.Textbox(label="输出信息", value="输出信息", interactive=False)

with gr.Blocks(
    theme=gr.Theme.load(r"E:\vs\MSST-WebUI\tools\themes\theme_blue.json")
    ) as demo:
    gr.Markdown('<div align="center"><font size=6><b>南京邮电大学本科毕业设计（论文）网上选题系统</b></font></div>')

    with gr.Tabs():
        with gr.TabItem(label="学生选题"):
            student()
        with gr.TabItem(label="教师管理"):
            teacher()
        with gr.TabItem(label="管理员选题"):
            admin()


demo.launch(inbrowser=True)