#include <iostream>  //输入输出头文件
#include <cstdlib>   //标准库头文件
#include <fstream>   //文件操作头文件
#include <string>    //字符串操作头文件
#include <sstream>   //字符串流头文件
#include <Windows.h> //windows头文件

#define MAX_LAB 8            // 实验室最大数量
#define MAX_APPOINTMENTS 200 // 预约最大条数

// 定义输出颜色
#define INFO_BLUE "\033[94m"
#define WARNING_YELLOW "\033[93m"
#define ERROR_RED "\033[91m"
#define RESET "\033[0m"

using namespace std;

// 实验室类型枚举
enum LabType
{
    HARDWARE = 0, // 硬件
    SOFTWARE = 1  // 软件
};

// 实验室规模枚举
enum LabSize
{
    SMALL = 40,
    MEDIUM = 60,
    LARGE = 80
};

// 实验室信息结构体
struct Lab
{
    int labNumber;       // 实验室编号
    LabType labType;     // 实验室类型
    LabSize labSize;     // 实验室规模
    bool schedule[7][9]; // 二维数组表示每天每时段的预约情况
    int startDate;       // 开始时间
    int endDate;         // 结束时间
};

// 添加预约信息结构体
struct Reservation
{
    string courseName;    // 课程名称
    string studentClass;  // 班级名称
    int date;             // 日期
    int startTime;        // 开始时间
    int endTime;          // 结束时间
    int requiredMachines; // 机器需求量
    LabType labType;      // 实验室类型
};

// 存储预约信息结构体
struct Appointment
{
    int date;            // 日期
    int startTime;       // 开始时间
    int endTime;         // 结束时间
    int labNumber;       // 实验室编号
    int labType;         // 实验室类型
    int labSize;         // 实验室规模
    string lessonName;   // 课程名称
    string studentClass; // 班级名称
};

// 函数声明
int importLabInfo(Lab labs[], int labCount);
void showLabInfo(const Lab labs[], int labCount);
void makeReservation(Lab labs[], int labCount, Reservation& reservation);
void writeAppointmentToFile(const Reservation& reservation, Lab labs[], int labCount);
bool makeReservationLogic(const Lab labs[], int labCount, int date, int startTime, int endTime, int requiredMachines);
bool makeReservationValuable(const Lab labs[], int labCount, const Reservation& reservation);
int readAppointment(Appointment appointments[], int maxAppointments);
void showAppointment(const Appointment appointments[], int count);
void cancelAppointment(Appointment appointments[], int& count);
void displayLabScheduleDate(const Appointment appointments[], int appointmentCount, int date);
void displayLabScheduleLab(const Appointment appointments[], int appointmentCount, int labNumber);
void exportLabSchedule(const Appointment appointments[], int appointmentCount, const Lab labs[], int labCount);
void showmenu();
void choosechoice(int choice, Lab labs[], Appointment appointments[]);

// 导入实验室信息，成功导入则返回实验室总数，导入失败返回0
int importLabInfo(Lab labs[], int labCount)
{
    // 打开文件
    ifstream inputFile("input.txt");

    // 如果文件不存在，则创建文件并提示用户输入
    if (!inputFile.is_open())
    {
        ofstream outputFile("input.txt");
        outputFile << "LabNumber,LabType,LabSize,StartDate,EndDate" << endl;
        cerr << ERROR_RED << "[ERROR]:文件 input.txt 不存在，已为您创建，请将实验室信息输入该文件中后重试" << RESET << endl;
        cout << endl;
        cout << INFO_BLUE << "[INFO]:按任意键关闭程序" << RESET << endl;
        cin.get();
        return 0;
    }

    // 读取标题行，但不使用
    string line;
    getline(inputFile, line);

    int count = 0;
    int lineCount = 0; // 用于计数文件的行数

    // 读取文件中的每一行，并将其转换为Lab对象
    while (getline(inputFile, line) && count < labCount)
    {
        lineCount++; // 每成功读取一行，行数加一
        stringstream ss(line);
        string token;

        // 逐个读取CSV格式的值
        getline(ss, token, ','); // LabNumber
        labs[count].labNumber = stoi(token);

        getline(ss, token, ','); // LabType
        labs[count].labType = static_cast<LabType>(stoi(token));

        getline(ss, token, ','); // LabSize
        labs[count].labSize = static_cast<LabSize>(stoi(token));

        getline(ss, token, ','); // StartDate
        labs[count].startDate = stoi(token);

        getline(ss, token, ','); // EndDate
        labs[count].endDate = stoi(token);

        // 将每个实验室的每个时间段都初始化为false
        for (int i = 0; i < 7; ++i)
        {
            for (int j = 0; j < 9; ++j)
            {
                labs[count].schedule[i][j] = false;
            }
        }

        count++;
    }

    // 关闭文件
    inputFile.close();
    // 行数检查
    if (lineCount < 8 || lineCount > 9)
    {
        cerr << ERROR_RED << "[ERROR]:文件行数不正确，请确保完整输入了8个实验室的数据" << RESET << endl;
        system("pause");
        return false;
    }
    cout << INFO_BLUE << "[INFO]:已成功读取到实验室信息..." << RESET << endl;
    return labCount;
}

// 输出实验室信息
void showLabInfo(const Lab labs[], int labCount)
{
    // 输出表头
    cout << WARNING_YELLOW << "编号\t类型\t容量\t开始时间\t结束时间" << RESET << endl;
    cout << "────────────────────────────────────────────────────" << endl;

    // 输出实验室信息
    for (int i = 0; i < labCount; ++i)
    {
        cout << labs[i].labNumber << '\t'
            << (labs[i].labType == HARDWARE ? "硬件" : "软件") << '\t'
            << labs[i].labSize << '\t'
            << labs[i].startDate << '\t'
            << labs[i].endDate << endl;
    }
    cout << "────────────────────────────────────────────────────" << endl;
}

// 预约实验室
void makeReservation(Lab labs[], int labCount, Reservation& reservation)
{
    // 声明一个变量，用于存储用户输入的实验室类型
    int labTypeInput;
    cout << INFO_BLUE << "[INFO]:请按顺序输入下述内容，并使用空格隔开" << RESET << endl;
    cout << endl;
    cout << "课程名称  班级  预约日期(YYYYMMDD)  开始时间(1-9)  结束时间(1-9)  机器数量  实验室类型(0: 硬件, 1: 软件)" << endl;
    // 获取用户输入的信息
    cin >> reservation.courseName >> reservation.studentClass >> reservation.date >> reservation.startTime >> reservation.endTime >> reservation.requiredMachines >> labTypeInput;

    // 检查用户输入的机器数量是否合理并按需求赋值(40,60,80)
    if (reservation.requiredMachines > 0 && reservation.requiredMachines <= 40)
    {
        reservation.requiredMachines = 40;
    }
    if (reservation.requiredMachines > 40 && reservation.requiredMachines <= 60)
    {
        reservation.requiredMachines = 60;
    }
    if (reservation.requiredMachines > 60 && reservation.requiredMachines <= 80)
    {
        reservation.requiredMachines = 80;
    }
    if (reservation.requiredMachines <= 0 && reservation.requiredMachines >= 80)
    {
        cerr << ERROR_RED << "[ERROR]:机器数量输入不合理，请输入(0-80)" << endl;
        return;
    }

    // 检查用户输入的实验室类型是否合理
    if (labTypeInput == 0 || labTypeInput == 1)
    {
        reservation.labType = static_cast<LabType>(labTypeInput);
    }
    else
    {
        cerr << ERROR_RED << "[ERROR]:实验室类型输入不合理，请输入(0: 硬件, 1: 软件)" << endl;
        return;
    }

    // 调用 makeReservationLogic 函数，检查预约是否合理
    if (makeReservationLogic(labs, labCount, reservation.date, reservation.startTime, reservation.endTime, reservation.requiredMachines) && makeReservationValuable(labs, labCount, reservation))
    {
        // 调用 writeAppointmentToFile 函数，将预约信息写入文件
        writeAppointmentToFile(reservation, labs, labCount);
    }
}

// 将预约信息写到文件
void writeAppointmentToFile(const Reservation& reservation, Lab labs[], int labCount)
{
    ofstream outFile("appointment.txt", ios::app); // 打开文件，追加写入
    if (!outFile.is_open())
    {
        // 如果文件不存在，则创建文件
        ofstream outputFile("appointment.txt");
        outputFile << "Date,StartTime,EndTime,LabNumber,LabType,LabSize,LessonName,Class" << endl;
        cerr << WARNING_YELLOW << "[WARNING]:未找到 appointment.txt，已重新创建" << RESET << endl;
    }

    // 查找符合条件的实验室，选择第一个符合条件的实验室
    int selectedLabIndex = -1;
    for (int i = 0; i < labCount; ++i)
    {
        if (labs[i].labType == reservation.labType && labs[i].labSize >= reservation.requiredMachines)
        {
            selectedLabIndex = i;
            break;
        }
    }

    if (selectedLabIndex != -1)
    {
        // 写入预约信息到文件
        outFile << reservation.date << "," << reservation.startTime << ","
            << reservation.endTime << "," << labs[selectedLabIndex].labNumber << ","
            << static_cast<int>(labs[selectedLabIndex].labType) << "," << static_cast<int>(labs[selectedLabIndex].labSize) << ","
            << reservation.courseName << "," << reservation.studentClass << "\n";

        // 更新实验室的预约情况，将对应时段标记为已预约
        for (int i = reservation.startTime - 1; i < reservation.endTime; ++i)
        {
            labs[selectedLabIndex].schedule[reservation.date % 7][i] = true;
        }

        cout << INFO_BLUE << "[INFO]:预约成功！" << RESET << endl;
    }
    else
    {
        cerr << ERROR_RED << "[ERROR]:没有符合条件的实验室可供预约" << endl;
    }

    outFile.close(); // 关闭文件
}

// 判断预约信息逻辑
bool makeReservationLogic(const Lab labs[], int labCount, int date, int startTime, int endTime, int requiredMachines)
{
    // 遍历所有实验室
    for (int labIndex = 0; labIndex < labCount; ++labIndex)
    {
        const Lab& lab = labs[labIndex];

        int reservationDate = date; // 预约日期的格式:YYYMMDD

        // 检查预约日期是否在实验室有效范围内
        if (reservationDate < lab.startDate || reservationDate > lab.endDate)
        {
            cerr << ERROR_RED << "[ERROR]:无效的预约日期" << endl;
            return false;
        }

        // 检查预约时间是否在有效范围内
        if (startTime < 1 || startTime > 9 || endTime < 1 || endTime > 9 || endTime <= startTime)
        {
            cerr << ERROR_RED << "[ERROR]:无效的预约时间" << endl;
            return false;
        }
    }

    // 如果通过了所有实验室的检查，表示预约成功
    return true;
}

// 判断预约输入是否有效
bool makeReservationValuable(const Lab labs[], int labCount, const Reservation& reservation)
{
    // 读取 "appointment.txt" 文件
    ifstream inputFile("appointment.txt");
    if (!inputFile.is_open())
    {
        // 如果文件不存在，则创建文件
        ofstream outputFile("appointment.txt");
        outputFile << "Date,StartTime,EndTime,LabNumber,LabType,LabSize,LessonName,Class" << endl;
        cerr << WARNING_YELLOW << "[WARNING]:未找到 appointment.txt，已重新创建" << RESET << endl;
    }

    string line;
    while (getline(inputFile, line))
    {
        stringstream ss(line);
        char comma;

        // 逐个读取CSV格式的值
        int date, startTime, endTime, labNumber, labType, labSize;
        string lessonName, studentClass;

        ss >> date >> comma >> startTime >> comma >> endTime >> comma >> labNumber >> comma >> labType >> comma >> labSize >> comma >> lessonName >> comma >> studentClass;

        // 检查实验室、日期和时间是否与现有的预约冲突
        if (labType == static_cast<int>(reservation.labType) &&
            date == reservation.date &&
            startTime <= reservation.endTime &&
            endTime >= reservation.startTime)
        {
            cerr << ERROR_RED << "[ERROR]:预约时间冲突，无法完成预约" << endl;
            inputFile.close();
            return false;
        }
    }

    inputFile.close();

    // 如果所有检查都通过，预约就是有效的
    return true;
}

// 读取预约记录文件，返回记录条数
int readAppointment(Appointment appointments[], int maxAppointments)
{
    // 打开文件
    ifstream inputFile("appointment.txt");

    // 如果文件不存在，则创建文件
    if (!inputFile.is_open())
    {
        // 如果文件不存在，则创建文件
        ofstream outputFile("appointment.txt");
        outputFile << "Date,StartTime,EndTime,LabNumber,LabType,LabSize,LessonName,Class" << endl;
        cerr << WARNING_YELLOW << "[WARNING]:未找到 appointment.txt，已重新创建" << RESET << endl;
        return 0;
    }

    // 读取文件中的记录
    int count = 0;
    string line;
    getline(inputFile, line); // 读取标题行，但不使用

    while (count < maxAppointments && getline(inputFile, line))
    {
        stringstream ss(line);
        char comma; // 用于读取逗号分隔符

        // 逐个读取CSV格式的值
        ss >> appointments[count].date >> comma >> appointments[count].startTime >> comma >> appointments[count].endTime >> comma >> appointments[count].labNumber >> comma >> appointments[count].labType >> comma >> appointments[count].labSize >> comma >> appointments[count].lessonName >> comma >> appointments[count].studentClass;

        count++;
    }

    inputFile.close();
    return count; // 返回记录条数
}

// 打印所有预约信息
void showAppointment(const Appointment appointments[], int count)
{
    // 打印预约信息表格的表头
    cout << WARNING_YELLOW << "日期\t\t时间\t实验室编号\t实验室类型\t实验室容量\t课程名称及班级" << RESET << endl;
    cout << "─────────────────────────────────────────────────────────────────────────────────────────" << endl;

    // 遍历所有预约信息，并打印
    for (int i = 0; i < count; ++i)
    {
        cout << appointments[i].date << '\t' << appointments[i].startTime << ' ' << '-' << ' ' << appointments[i].endTime
            << '\t' << appointments[i].labNumber << '\t' << '\t' << (appointments[i].labType == 0 ? "硬件" : "软件")
            << '\t' << '\t' << appointments[i].labSize << '\t' << '\t' << appointments[i].lessonName << appointments[i].studentClass << endl;
    }
}

// 取消预约
void cancelAppointment(Appointment appointments[], int& count)
{
    // 输入要取消的预约信息
    int cancelDate, cancelStartTime, cancelEndTime;

    cout << INFO_BLUE << "[INFO]:请按顺序输入下述内容，并使用空格隔开" << RESET << endl;
    cout << endl;
    cout << "取消预约的日期(YYYYMMDD)  课程开始时间(1-9)  课程结束时间(1-9)" << endl;
    cin >> cancelDate >> cancelStartTime >> cancelEndTime;

    // 使用 remove_if 移动匹配的元素到末尾
    auto it = remove_if(appointments, appointments + count,
        [cancelDate, cancelStartTime, cancelEndTime](const Appointment& app)
        {
            return app.date == cancelDate && app.startTime == cancelStartTime && app.endTime == cancelEndTime;
        });

    // 根据 remove_if 的返回值计算新的有效元素数量
    int newCount = distance(appointments, it);

    if (newCount < count)
    {
        cout << endl;
        cout << INFO_BLUE << "[INFO]:取消预约成功！" << RESET << endl;
        // 将预约信息写入文件
        ofstream outFile("appointment.txt");
        if (outFile.is_open())
        {
            outFile << "Date,StartTime,EndTime,LabNumber,LabType,LabSize,LessonName,Class" << endl;
            for (int i = 0; i < newCount; ++i)
            {
                outFile << appointments[i].date << ","
                    << appointments[i].startTime << ","
                    << appointments[i].endTime << ","
                    << appointments[i].labNumber << ","
                    << appointments[i].labType << ","
                    << appointments[i].labSize << ","
                    << appointments[i].lessonName << ","
                    << appointments[i].studentClass << endl;
            }
            outFile.close();
        }

        count = newCount;
    }
    else
    {
        cout << endl;
        cerr << ERROR_RED << "[ERROR]:取消预约失败，未找到匹配的预约信息!" << RESET << endl;
    }
}

// 按日期输出预约信息
void displayLabScheduleDate(const Appointment appointments[], int appointmentCount, int date)
{
    // 创建二维数组来表示预约情况
    const int MAX_LABS = 8;
    const int MAX_TIMESLOTS = 9;

    // 创建二维数组来表示预约情况
    char schedule[MAX_LABS][MAX_TIMESLOTS];

    // 初始化预约情况数组
    for (int i = 0; i < MAX_LABS; ++i)
    {
        for (int j = 0; j < MAX_TIMESLOTS; ++j)
        {
            schedule[i][j] = ' ';
        }
    }

    // 根据预约信息更新预约情况数组
    for (int i = 0; i < appointmentCount; ++i)
    {
        if (appointments[i].date == date)
        {
            int labIndex = appointments[i].labNumber - 1;
            int startTime = appointments[i].startTime - 1;
            int endTime = appointments[i].endTime;

            for (int j = startTime; j < endTime; ++j)
            {
                schedule[labIndex][j] = 'O';
            }
        }
    }

    // 输出日期和预约情况
    cout << endl;
    cout << WARNING_YELLOW << "日期 " << INFO_BLUE << date << WARNING_YELLOW << " 预约信息如下：" << RESET << endl;
    cout << endl;
    cout << WARNING_YELLOW << "实验室\t\t1\t2\t3\t4\t5\t6\t7\t8" << RESET << endl;
    cout << "────────────────────────────────────────────────────────────────────────────────" << endl;

    for (int i = 0; i < MAX_TIMESLOTS; ++i)
    {
        cout << "时间段" << i + 1 << "\t\t";
        for (int j = 0; j < MAX_LABS; ++j)
        {
            if (schedule[j][i] == ' ')
            {
                cout << "可预约\t";
            }
            else
            {
                cout << schedule[j][i] << "\t";
            }
        }
        cout << endl;
    }
    cout << "────────────────────────────────────────────────────────────────────────────────" << endl;
}

// 按实验室编号输出预约信息
void displayLabScheduleLab(const Appointment appointments[], int appointmentCount, int labNumber)
{
    const int MAX_TIMESLOTS = 9;

    // 创建二维数组来表示预约情况
    char schedule[MAX_TIMESLOTS][7];

    // 初始化预约情况数组
    for (int i = 0; i < MAX_TIMESLOTS; ++i)
    {
        for (int j = 0; j < 7; ++j)
        {
            schedule[i][j] = ' ';
        }
    }

    // 根据预约信息更新预约情况数组
    for (int i = 0; i < appointmentCount; ++i)
    {
        if (appointments[i].labNumber == labNumber)
        {
            int startTime = appointments[i].startTime - 1;
            int endTime = appointments[i].endTime;

            for (int j = startTime; j < endTime; ++j)
            {
                int dayOfWeek = appointments[i].date % 7;
                schedule[j][dayOfWeek] = 'O';
            }
        }
    }

    // 输出实验室编号和预约情况
    cout << endl;
    cout << WARNING_YELLOW << "实验室 " << INFO_BLUE << labNumber << WARNING_YELLOW << " 的预约信息如下：" << RESET << endl;
    cout << endl;
    cout << "星期\t\t1\t2\t3\t4\t5\t6\t7" << endl;
    cout << "────────────────────────────────────────────────────────────────────────" << endl;

    for (int i = 0; i < MAX_TIMESLOTS; ++i)
    {
        cout << "时间段" << i + 1 << "\t\t";
        for (int j = 0; j < 7; ++j)
        {
            if (schedule[i][j] == ' ')
            {
                cout << "可预约\t";
            }
            else
            {
                cout << schedule[i][j] << "\t";
            }
        }
        cout << endl;
    }
    cout << "────────────────────────────────────────────────────────────────────────" << endl;
}

// 导出实验室课表
void exportLabSchedule(const Appointment appointments[], int appointmentCount, const Lab labs[], int labCount)
{
    // 每个时间段有9个时间段
    const int MAX_TIMESLOTS = 9;
    // 每个星期有7个时间段
    const int MAX_DAYS = 7;

    // 创建文件输出流
    ofstream outputFile("output.txt");

    // 遍历每个实验室
    for (int labIndex = 0; labIndex < labCount; ++labIndex)
    {
        const Lab& lab = labs[labIndex];
        outputFile << "                                             ";
        outputFile << "实验室" << lab.labNumber << "，类型：";
        outputFile << (lab.labType == HARDWARE ? "硬件" : "软件");
        outputFile << "，机位总数：" << lab.labSize << "，课表" << endl;
        outputFile << endl;

        // 创建二维数组来表示课表
        string schedule[MAX_TIMESLOTS][MAX_DAYS];

        // 初始化课表为空
        for (int i = 0; i < MAX_TIMESLOTS; ++i)
        {
            for (int j = 0; j < MAX_DAYS; ++j)
            {
                schedule[i][j] = "";
            }
        }

        // 填充课表
        for (int appointmentIndex = 0; appointmentIndex < appointmentCount; ++appointmentIndex)
        {
            const Appointment& appointment = appointments[appointmentIndex];

            // 如果预约的实验室与当前实验室相同
            if (appointment.labNumber == lab.labNumber)
            {
                int startTime = appointment.startTime - 1;
                int endTime = appointment.endTime;

                // 遍历预约的时间段
                for (int j = startTime; j < endTime; ++j)
                {
                    int dayOfWeek = appointment.date % 7;
                    schedule[j][dayOfWeek] = appointment.lessonName;
                }
            }
        }

        // 输出课表到文件
        outputFile << "─────────────────────────────────────────────────────────────────────────────────────────────" << endl;
        outputFile << "星期\t\t1\t\t2\t\t3\t\t4\t\t5\t\t6\t\t7" << endl;

        for (int i = 0; i < MAX_TIMESLOTS; ++i)
        {
            outputFile << "时间段" << i + 1 << "\t\t";
            for (int j = 0; j < MAX_DAYS; ++j)
            {
                if (schedule[i][j] != "")
                {
                    outputFile << schedule[i][j];
                }
                outputFile << "\t\t";
            }
            outputFile << endl;
        }
        outputFile << "================================================================================================================================" << endl;
        outputFile << endl;
        outputFile << endl;
    }

    outputFile.close();
}

// 打印主菜单
void showmenu()
{
    cout << "──────────────────────────────" << WARNING_YELLOW << " 欢迎使用实验室预约系统! " << RESET << "───────────────────────────────" << endl;
    cout << "                                                                  当前版本:v1.2.1214 " << endl;
    cout << "                            1.   显示所有实验室的信息" << endl;
    cout << "                            2.       预约实验室" << endl;
    cout << "                            3.        取消预约" << endl;
    cout << "                            4.    显示所有预约信息" << endl;
    cout << "                            5. 按日期查询实验室预约情况" << endl;
    cout << "                            6. 按实验室编号查询预约情况" << endl;
    cout << "                            7.   导出实验室课表到文件" << endl;
    cout << "                            0.        退出程序" << endl;
    cout << endl;
    cout << "──────────────────────────────────────────────────────────────────────────────────────" << endl;
    cout << endl;
    cout << INFO_BLUE << "[INFO]:请输入你的选择[0-4]:" << RESET;
    return;
}

// 处理用户选择
void choosechoice(int choice, Lab labs[], Appointment appointments[])
{
    switch (choice)
    {
    case 1:
    {
        cout << WARNING_YELLOW << "──────────────── 当前位于：1.显示所有实验室的信息 ────────────────" << RESET << endl;
        cout << endl;
        int labCount;
        labCount = importLabInfo(labs, MAX_LAB);
        cout << endl;
        showLabInfo(labs, labCount);
        cout << endl;
        cout << INFO_BLUE << "[INFO]:按任意键返回主界面..." << RESET << endl;
        cin.get();
        cin.get();
        system("cls");
        break;
    }
    case 2:
    {
        char temp = ' ';
        do
        {
            cout << WARNING_YELLOW << "──────────────── 当前位于：2.预约实验室 ────────────────" << RESET << endl;
            cout << endl;
            Reservation reservation;
            makeReservation(labs, MAX_LAB, reservation);
            cout << endl;
            cout << INFO_BLUE << "[INFO]:继续预约?(Y/N)" << RESET;
            cin >> temp;
            system("cls");
        } while (temp == 'Y' || temp == 'y');
        break;
    }
    case 3:
    {
        cout << WARNING_YELLOW << "──────────────── 当前位于：3.取消预约 ────────────────" << RESET << endl;
        cout << endl;
        int count = readAppointment(appointments, MAX_APPOINTMENTS);
        cancelAppointment(appointments, count);
        cout << endl;
        cout << INFO_BLUE << "[INFO]:按任意键返回主界面..." << RESET << endl;
        cin.get();
        cin.get();
        system("cls");
        break;
    }
    case 4:
    {
        cout << WARNING_YELLOW << "──────────────── 当前位于：4.显示所有预约信息 ────────────────" << RESET << endl;
        cout << endl;
        int count = readAppointment(appointments, MAX_APPOINTMENTS);
        showAppointment(appointments, count);
        cout << endl;
        cout << INFO_BLUE << "[INFO]:按任意键返回主界面..." << RESET << endl;
        cin.get();
        cin.get();
        system("cls");
        break;
    }
    case 5:
    {
        char temp = ' ';
        do
        {
            cout << WARNING_YELLOW << "──────────────── 当前位于：5. 按日期查询实验室预约情况 ────────────────" << RESET << endl;
            int date;
            cout << endl;
            cout << "[INFO]:请输入要查询的日期(YYYMMDD): ";
            cin >> date;
            int appointmentCount = readAppointment(appointments, MAX_APPOINTMENTS);
            displayLabScheduleDate(appointments, appointmentCount, date);
            cout << endl;
            cout << INFO_BLUE << "[INFO]:继续查询?(Y/N)" << RESET;
            cin >> temp;
            system("cls");
        } while (temp == 'Y' || temp == 'y');
        break;
    }
    case 6:
    {
        char temp = ' ';
        do
        {
            cout << WARNING_YELLOW << "──────────────── 当前位于：6. 按实验室编号查询预约情况 ────────────────" << RESET << endl;
            cout << endl;
            int labindex;
            cout << "[INFO]:请输入要查询的实验室编号(1-8): ";
            cin >> labindex;
            int appointmentCount = readAppointment(appointments, MAX_APPOINTMENTS);
            displayLabScheduleLab(appointments, appointmentCount, labindex);
            cout << endl;
            cout << INFO_BLUE << "[INFO]:继续查询?(Y/N)" << RESET;
            cin >> temp;
            system("cls");
        } while (temp == 'Y' || temp == 'y');
        break;
    }
    case 7:
    {
        cout << WARNING_YELLOW << "──────────────── 当前位于：7. 导出实验室课表到文件 ────────────────" << RESET << endl;
        cout << endl;
        int appointmentCount = readAppointment(appointments, MAX_APPOINTMENTS);
        exportLabSchedule(appointments, appointmentCount, labs, MAX_LAB);
        cout << "已成功输出课表到output.txt中";
        cout << endl;
        cout << INFO_BLUE << "[INFO]:按任意键返回主界面..." << RESET << endl;
        cin.get();
        cin.get();
        system("cls");
        break;
    }
    case 0:
    {
        cout << INFO_BLUE << "[INFO]:欢迎下次使用，再见！" << endl;
        MessageBox(NULL, L"欢迎下次使用，再见！", L"退出", MB_OK);
        return;
    }
    }
}

int main()
{
    // 定义数组，用于存储实验室信息
    Lab labs[MAX_LAB];
    // 定义数组，用于存储预约信息
    Appointment appointments[MAX_APPOINTMENTS];

    // 读取实验室信息
    if (!importLabInfo(labs, MAX_LAB))
    {
        return 0;
    }
    Sleep(500);
    system("cls");

    // 定义一个变量，用于存储用户输入的选项
    int choice;
    // 循环执行，直到用户输入0
    do
    {
        // 显示菜单
        showmenu();
        // 获取用户输入的选项
        cin >> choice;
        system("cls");
        // 根据用户输入的选项，调用choosechoice函数
        choosechoice(choice, labs, appointments);
    } while (choice != 0);
    return 0;
}
