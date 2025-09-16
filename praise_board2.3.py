import tkinter as tk
from tkinter import font, ttk
import functools
import time

class PraiseBoard:
    def __init__(self, root):
        self.root = root
        self.root.title('班级表扬榜')
        self.root.configure(bg='#87CEED')
        
        # 模式状态变量
        self.mode = tk.StringVar(value='praise')
        self.students = {}
        
        # 模式选择控件
        # 创建标题框架
        title_frame = tk.Frame(root, bg='#87CEED')
        title_frame.pack(fill='x', padx=20, pady=10)

        # 模式选择控件
        mode_frame = tk.Frame(title_frame, bg='#87CEED')
        mode_frame.pack(side='left', pady=10)

        # 学科下拉菜单
        self.subject_combo = ttk.Combobox(
            title_frame,
            values=['语文','数学','英语','物理','化学','政治','历史','地理','生物','请输入文本'],
            font=('宋体', 30),
            state='readonly',
            width=10
        )
        self.subject_combo.pack(side='left', padx=20)
        
        
        tk.Radiobutton(mode_frame, text='表扬模式', variable=self.mode, value='praise',
                      font=('宋体', 18), bg='#87CEED').pack(side='left', padx=20)
        tk.Radiobutton(mode_frame, text='批评模式', variable=self.mode, value='criticism',
                      font=('宋体', 18), bg='#87CEED').pack(side='left', padx=20)

        main_frame = tk.Frame(root, bg='#87CEED')
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # 创建6列分组框架
        for group_num in range(6):
            group_frame = tk.Frame(main_frame, bg='#87CEED')
            group_frame.grid(row=0, column=group_num, padx=10, sticky='nsew')
            main_frame.grid_columnconfigure(group_num, weight=1)
            main_frame.grid_rowconfigure(0, weight=1)
            
            # 修改分组标题文本为"第1,2组"格式
            group_title = f'第{group_num*2+1},{group_num*2+2}组'
            tk.Label(group_frame, 
                    text=group_title,
                    font=('黑体', 30, 'bold'),
                    bg='#87CEED',
                    pady=10).pack(side='bottom', anchor='s', fill='x')
            
            # 创建组内学生容器（后打包填充上方空间）
            student_container = tk.Frame(group_frame, bg='#87CEED')
            student_container.pack(fill='both', expand=True)
            
        # 从文件按分组读取学生姓名
        with open('students_name.txt', 'r') as f:
            all_students = [name.strip() for name in f.readlines()]
            groups = [all_students[i*8:(i+1)*8] for i in range(6)]

        # 动态生成学生标签
        for group_idx, group_students in enumerate(groups):
            group_frame = main_frame.winfo_children()[group_idx]
            student_container = group_frame.winfo_children()[1]
            
            for student_idx, student_name in enumerate(group_students):
                # 创建学生条目容器
                container = tk.Frame(student_container, bg='#87CEED')
                container.pack(fill='x', pady=2)
            
                # 学生姓名标签
                lbl = tk.Label(container,
                            text=student_name,
                            font=('仿宋', 30),
                            padx=10,
                            pady=10,
                            relief='ridge')
                lbl.pack(side='left')
                lbl.bind('<Button-1>', functools.partial(self.toggle_check, student_name))
                
                # 对勾标签
                check_label = tk.Label(container,
                                      text='',
                                      font=('Arial', 30),
                                      fg='green',
                                      padx=10,
                                      bg='#87CEED')
                check_label.pack(side='left', padx=5)
                
                # 初始化状态存储（添加倍数字段）
                self.students[student_name] = {
                    'praise': tk.BooleanVar(value=False),
                    'criticism': tk.BooleanVar(value=False),
                            'check_label': check_label,
                }
        
        # 时间显示标签
        self.time_label = tk.Label(title_frame,
                                text='班级实时表现公示栏',
                                font=('黑体', 30, 'bold'),
                                bg='#87CEED',
                                padx=20,
                                pady=15)
        self.time_label.pack(side='left', expand=True, fill='x')
        self.time_label.pack(side='right', padx=20)
        self.update_time()

    def update_time(self):
        weekday_map = {'0':'日', '1':'一', '2':'二', '3':'三', '4':'四', '5':'五', '6':'六'}
        current_time = time.strftime('%Y年%m月%d日 %H:%M:%S 星期') + weekday_map[time.strftime('%w')]
        current_time = current_time.replace('星期0', '星期日')
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)


    def toggle_mode(self):
        # 切换模式时更新所有学生显示
        for student in self.students:
            self.update_check_display(student)

    def toggle_check(self, student, event=None):
        current_mode = self.mode.get()
        current_state = self.students[student][current_mode].get()
        self.students[student][current_mode].set(not current_state)
        
        symbol = '✓' if current_mode == 'praise' else '✗'
        color = 'green' if current_mode == 'praise' else 'red'
        display_text = symbol if not current_state else ''
        self.students[student]['check_label'].config(
            text=display_text,
            fg=color
        )

    def update_check_display(self, student):
        current_mode = self.mode.get()
        state = self.students[student][current_mode].get()
        symbol = '✓' if current_mode == 'praise' else '✗'
        color = 'green' if current_mode == 'praise' else 'red'
        display_text = symbol if not state else ''
        self.students[student]['check_label'].config(
            text=display_text,
            fg=color
        )


if __name__ == '__main__':
    root = tk.Tk()
    app = PraiseBoard(root)
    root.mainloop()
