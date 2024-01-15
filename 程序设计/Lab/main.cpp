#include <iostream>  //�������ͷ�ļ�
#include <cstdlib>   //��׼��ͷ�ļ�
#include <fstream>   //�ļ�����ͷ�ļ�
#include <string>    //�ַ�������ͷ�ļ�
#include <sstream>   //�ַ�����ͷ�ļ�
#include <Windows.h> //windowsͷ�ļ�

#define MAX_LAB 8            // ʵ�����������
#define MAX_APPOINTMENTS 200 // ԤԼ�������

// ���������ɫ
#define INFO_BLUE "\033[94m"
#define WARNING_YELLOW "\033[93m"
#define ERROR_RED "\033[91m"
#define RESET "\033[0m"

using namespace std;

// ʵ��������ö��
enum LabType
{
    HARDWARE = 0, // Ӳ��
    SOFTWARE = 1  // ���
};

// ʵ���ҹ�ģö��
enum LabSize
{
    SMALL = 40,
    MEDIUM = 60,
    LARGE = 80
};

// ʵ������Ϣ�ṹ��
struct Lab
{
    int labNumber;       // ʵ���ұ��
    LabType labType;     // ʵ��������
    LabSize labSize;     // ʵ���ҹ�ģ
    bool schedule[7][9]; // ��ά�����ʾÿ��ÿʱ�ε�ԤԼ���
    int startDate;       // ��ʼʱ��
    int endDate;         // ����ʱ��
};

// ���ԤԼ��Ϣ�ṹ��
struct Reservation
{
    string courseName;    // �γ�����
    string studentClass;  // �༶����
    int date;             // ����
    int startTime;        // ��ʼʱ��
    int endTime;          // ����ʱ��
    int requiredMachines; // ����������
    LabType labType;      // ʵ��������
};

// �洢ԤԼ��Ϣ�ṹ��
struct Appointment
{
    int date;            // ����
    int startTime;       // ��ʼʱ��
    int endTime;         // ����ʱ��
    int labNumber;       // ʵ���ұ��
    int labType;         // ʵ��������
    int labSize;         // ʵ���ҹ�ģ
    string lessonName;   // �γ�����
    string studentClass; // �༶����
};

// ��������
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

// ����ʵ������Ϣ���ɹ������򷵻�ʵ��������������ʧ�ܷ���0
int importLabInfo(Lab labs[], int labCount)
{
    // ���ļ�
    ifstream inputFile("input.txt");

    // ����ļ������ڣ��򴴽��ļ�����ʾ�û�����
    if (!inputFile.is_open())
    {
        ofstream outputFile("input.txt");
        outputFile << "LabNumber,LabType,LabSize,StartDate,EndDate" << endl;
        cerr << ERROR_RED << "[ERROR]:�ļ� input.txt �����ڣ���Ϊ���������뽫ʵ������Ϣ������ļ��к�����" << RESET << endl;
        cout << endl;
        cout << INFO_BLUE << "[INFO]:��������رճ���" << RESET << endl;
        cin.get();
        return 0;
    }

    // ��ȡ�����У�����ʹ��
    string line;
    getline(inputFile, line);

    int count = 0;
    int lineCount = 0; // ���ڼ����ļ�������

    // ��ȡ�ļ��е�ÿһ�У�������ת��ΪLab����
    while (getline(inputFile, line) && count < labCount)
    {
        lineCount++; // ÿ�ɹ���ȡһ�У�������һ
        stringstream ss(line);
        string token;

        // �����ȡCSV��ʽ��ֵ
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

        // ��ÿ��ʵ���ҵ�ÿ��ʱ��ζ���ʼ��Ϊfalse
        for (int i = 0; i < 7; ++i)
        {
            for (int j = 0; j < 9; ++j)
            {
                labs[count].schedule[i][j] = false;
            }
        }

        count++;
    }

    // �ر��ļ�
    inputFile.close();
    // �������
    if (lineCount < 8 || lineCount > 9)
    {
        cerr << ERROR_RED << "[ERROR]:�ļ���������ȷ����ȷ������������8��ʵ���ҵ�����" << RESET << endl;
        system("pause");
        return false;
    }
    cout << INFO_BLUE << "[INFO]:�ѳɹ���ȡ��ʵ������Ϣ..." << RESET << endl;
    return labCount;
}

// ���ʵ������Ϣ
void showLabInfo(const Lab labs[], int labCount)
{
    // �����ͷ
    cout << WARNING_YELLOW << "���\t����\t����\t��ʼʱ��\t����ʱ��" << RESET << endl;
    cout << "��������������������������������������������������������������������������������������������������������" << endl;

    // ���ʵ������Ϣ
    for (int i = 0; i < labCount; ++i)
    {
        cout << labs[i].labNumber << '\t'
            << (labs[i].labType == HARDWARE ? "Ӳ��" : "���") << '\t'
            << labs[i].labSize << '\t'
            << labs[i].startDate << '\t'
            << labs[i].endDate << endl;
    }
    cout << "��������������������������������������������������������������������������������������������������������" << endl;
}

// ԤԼʵ����
void makeReservation(Lab labs[], int labCount, Reservation& reservation)
{
    // ����һ�����������ڴ洢�û������ʵ��������
    int labTypeInput;
    cout << INFO_BLUE << "[INFO]:�밴˳�������������ݣ���ʹ�ÿո����" << RESET << endl;
    cout << endl;
    cout << "�γ�����  �༶  ԤԼ����(YYYYMMDD)  ��ʼʱ��(1-9)  ����ʱ��(1-9)  ��������  ʵ��������(0: Ӳ��, 1: ���)" << endl;
    // ��ȡ�û��������Ϣ
    cin >> reservation.courseName >> reservation.studentClass >> reservation.date >> reservation.startTime >> reservation.endTime >> reservation.requiredMachines >> labTypeInput;

    // ����û�����Ļ��������Ƿ����������ֵ(40,60,80)
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
        cerr << ERROR_RED << "[ERROR]:�����������벻����������(0-80)" << endl;
        return;
    }

    // ����û������ʵ���������Ƿ����
    if (labTypeInput == 0 || labTypeInput == 1)
    {
        reservation.labType = static_cast<LabType>(labTypeInput);
    }
    else
    {
        cerr << ERROR_RED << "[ERROR]:ʵ�����������벻����������(0: Ӳ��, 1: ���)" << endl;
        return;
    }

    // ���� makeReservationLogic ���������ԤԼ�Ƿ����
    if (makeReservationLogic(labs, labCount, reservation.date, reservation.startTime, reservation.endTime, reservation.requiredMachines) && makeReservationValuable(labs, labCount, reservation))
    {
        // ���� writeAppointmentToFile ��������ԤԼ��Ϣд���ļ�
        writeAppointmentToFile(reservation, labs, labCount);
    }
}

// ��ԤԼ��Ϣд���ļ�
void writeAppointmentToFile(const Reservation& reservation, Lab labs[], int labCount)
{
    ofstream outFile("appointment.txt", ios::app); // ���ļ���׷��д��
    if (!outFile.is_open())
    {
        // ����ļ������ڣ��򴴽��ļ�
        ofstream outputFile("appointment.txt");
        outputFile << "Date,StartTime,EndTime,LabNumber,LabType,LabSize,LessonName,Class" << endl;
        cerr << WARNING_YELLOW << "[WARNING]:δ�ҵ� appointment.txt�������´���" << RESET << endl;
    }

    // ���ҷ���������ʵ���ң�ѡ���һ������������ʵ����
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
        // д��ԤԼ��Ϣ���ļ�
        outFile << reservation.date << "," << reservation.startTime << ","
            << reservation.endTime << "," << labs[selectedLabIndex].labNumber << ","
            << static_cast<int>(labs[selectedLabIndex].labType) << "," << static_cast<int>(labs[selectedLabIndex].labSize) << ","
            << reservation.courseName << "," << reservation.studentClass << "\n";

        // ����ʵ���ҵ�ԤԼ���������Ӧʱ�α��Ϊ��ԤԼ
        for (int i = reservation.startTime - 1; i < reservation.endTime; ++i)
        {
            labs[selectedLabIndex].schedule[reservation.date % 7][i] = true;
        }

        cout << INFO_BLUE << "[INFO]:ԤԼ�ɹ���" << RESET << endl;
    }
    else
    {
        cerr << ERROR_RED << "[ERROR]:û�з���������ʵ���ҿɹ�ԤԼ" << endl;
    }

    outFile.close(); // �ر��ļ�
}

// �ж�ԤԼ��Ϣ�߼�
bool makeReservationLogic(const Lab labs[], int labCount, int date, int startTime, int endTime, int requiredMachines)
{
    // ��������ʵ����
    for (int labIndex = 0; labIndex < labCount; ++labIndex)
    {
        const Lab& lab = labs[labIndex];

        int reservationDate = date; // ԤԼ���ڵĸ�ʽ:YYYMMDD

        // ���ԤԼ�����Ƿ���ʵ������Ч��Χ��
        if (reservationDate < lab.startDate || reservationDate > lab.endDate)
        {
            cerr << ERROR_RED << "[ERROR]:��Ч��ԤԼ����" << endl;
            return false;
        }

        // ���ԤԼʱ���Ƿ�����Ч��Χ��
        if (startTime < 1 || startTime > 9 || endTime < 1 || endTime > 9 || endTime <= startTime)
        {
            cerr << ERROR_RED << "[ERROR]:��Ч��ԤԼʱ��" << endl;
            return false;
        }
    }

    // ���ͨ��������ʵ���ҵļ�飬��ʾԤԼ�ɹ�
    return true;
}

// �ж�ԤԼ�����Ƿ���Ч
bool makeReservationValuable(const Lab labs[], int labCount, const Reservation& reservation)
{
    // ��ȡ "appointment.txt" �ļ�
    ifstream inputFile("appointment.txt");
    if (!inputFile.is_open())
    {
        // ����ļ������ڣ��򴴽��ļ�
        ofstream outputFile("appointment.txt");
        outputFile << "Date,StartTime,EndTime,LabNumber,LabType,LabSize,LessonName,Class" << endl;
        cerr << WARNING_YELLOW << "[WARNING]:δ�ҵ� appointment.txt�������´���" << RESET << endl;
    }

    string line;
    while (getline(inputFile, line))
    {
        stringstream ss(line);
        char comma;

        // �����ȡCSV��ʽ��ֵ
        int date, startTime, endTime, labNumber, labType, labSize;
        string lessonName, studentClass;

        ss >> date >> comma >> startTime >> comma >> endTime >> comma >> labNumber >> comma >> labType >> comma >> labSize >> comma >> lessonName >> comma >> studentClass;

        // ���ʵ���ҡ����ں�ʱ���Ƿ������е�ԤԼ��ͻ
        if (labType == static_cast<int>(reservation.labType) &&
            date == reservation.date &&
            startTime <= reservation.endTime &&
            endTime >= reservation.startTime)
        {
            cerr << ERROR_RED << "[ERROR]:ԤԼʱ���ͻ���޷����ԤԼ" << endl;
            inputFile.close();
            return false;
        }
    }

    inputFile.close();

    // ������м�鶼ͨ����ԤԼ������Ч��
    return true;
}

// ��ȡԤԼ��¼�ļ������ؼ�¼����
int readAppointment(Appointment appointments[], int maxAppointments)
{
    // ���ļ�
    ifstream inputFile("appointment.txt");

    // ����ļ������ڣ��򴴽��ļ�
    if (!inputFile.is_open())
    {
        // ����ļ������ڣ��򴴽��ļ�
        ofstream outputFile("appointment.txt");
        outputFile << "Date,StartTime,EndTime,LabNumber,LabType,LabSize,LessonName,Class" << endl;
        cerr << WARNING_YELLOW << "[WARNING]:δ�ҵ� appointment.txt�������´���" << RESET << endl;
        return 0;
    }

    // ��ȡ�ļ��еļ�¼
    int count = 0;
    string line;
    getline(inputFile, line); // ��ȡ�����У�����ʹ��

    while (count < maxAppointments && getline(inputFile, line))
    {
        stringstream ss(line);
        char comma; // ���ڶ�ȡ���ŷָ���

        // �����ȡCSV��ʽ��ֵ
        ss >> appointments[count].date >> comma >> appointments[count].startTime >> comma >> appointments[count].endTime >> comma >> appointments[count].labNumber >> comma >> appointments[count].labType >> comma >> appointments[count].labSize >> comma >> appointments[count].lessonName >> comma >> appointments[count].studentClass;

        count++;
    }

    inputFile.close();
    return count; // ���ؼ�¼����
}

// ��ӡ����ԤԼ��Ϣ
void showAppointment(const Appointment appointments[], int count)
{
    // ��ӡԤԼ��Ϣ���ı�ͷ
    cout << WARNING_YELLOW << "����\t\tʱ��\tʵ���ұ��\tʵ��������\tʵ��������\t�γ����Ƽ��༶" << RESET << endl;
    cout << "����������������������������������������������������������������������������������������������������������������������������������������������������������������������������������" << endl;

    // ��������ԤԼ��Ϣ������ӡ
    for (int i = 0; i < count; ++i)
    {
        cout << appointments[i].date << '\t' << appointments[i].startTime << ' ' << '-' << ' ' << appointments[i].endTime
            << '\t' << appointments[i].labNumber << '\t' << '\t' << (appointments[i].labType == 0 ? "Ӳ��" : "���")
            << '\t' << '\t' << appointments[i].labSize << '\t' << '\t' << appointments[i].lessonName << appointments[i].studentClass << endl;
    }
}

// ȡ��ԤԼ
void cancelAppointment(Appointment appointments[], int& count)
{
    // ����Ҫȡ����ԤԼ��Ϣ
    int cancelDate, cancelStartTime, cancelEndTime;

    cout << INFO_BLUE << "[INFO]:�밴˳�������������ݣ���ʹ�ÿո����" << RESET << endl;
    cout << endl;
    cout << "ȡ��ԤԼ������(YYYYMMDD)  �γ̿�ʼʱ��(1-9)  �γ̽���ʱ��(1-9)" << endl;
    cin >> cancelDate >> cancelStartTime >> cancelEndTime;

    // ʹ�� remove_if �ƶ�ƥ���Ԫ�ص�ĩβ
    auto it = remove_if(appointments, appointments + count,
        [cancelDate, cancelStartTime, cancelEndTime](const Appointment& app)
        {
            return app.date == cancelDate && app.startTime == cancelStartTime && app.endTime == cancelEndTime;
        });

    // ���� remove_if �ķ���ֵ�����µ���ЧԪ������
    int newCount = distance(appointments, it);

    if (newCount < count)
    {
        cout << endl;
        cout << INFO_BLUE << "[INFO]:ȡ��ԤԼ�ɹ���" << RESET << endl;
        // ��ԤԼ��Ϣд���ļ�
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
        cerr << ERROR_RED << "[ERROR]:ȡ��ԤԼʧ�ܣ�δ�ҵ�ƥ���ԤԼ��Ϣ!" << RESET << endl;
    }
}

// ���������ԤԼ��Ϣ
void displayLabScheduleDate(const Appointment appointments[], int appointmentCount, int date)
{
    // ������ά��������ʾԤԼ���
    const int MAX_LABS = 8;
    const int MAX_TIMESLOTS = 9;

    // ������ά��������ʾԤԼ���
    char schedule[MAX_LABS][MAX_TIMESLOTS];

    // ��ʼ��ԤԼ�������
    for (int i = 0; i < MAX_LABS; ++i)
    {
        for (int j = 0; j < MAX_TIMESLOTS; ++j)
        {
            schedule[i][j] = ' ';
        }
    }

    // ����ԤԼ��Ϣ����ԤԼ�������
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

    // ������ں�ԤԼ���
    cout << endl;
    cout << WARNING_YELLOW << "���� " << INFO_BLUE << date << WARNING_YELLOW << " ԤԼ��Ϣ���£�" << RESET << endl;
    cout << endl;
    cout << WARNING_YELLOW << "ʵ����\t\t1\t2\t3\t4\t5\t6\t7\t8" << RESET << endl;
    cout << "����������������������������������������������������������������������������������������������������������������������������������������������������������������" << endl;

    for (int i = 0; i < MAX_TIMESLOTS; ++i)
    {
        cout << "ʱ���" << i + 1 << "\t\t";
        for (int j = 0; j < MAX_LABS; ++j)
        {
            if (schedule[j][i] == ' ')
            {
                cout << "��ԤԼ\t";
            }
            else
            {
                cout << schedule[j][i] << "\t";
            }
        }
        cout << endl;
    }
    cout << "����������������������������������������������������������������������������������������������������������������������������������������������������������������" << endl;
}

// ��ʵ���ұ�����ԤԼ��Ϣ
void displayLabScheduleLab(const Appointment appointments[], int appointmentCount, int labNumber)
{
    const int MAX_TIMESLOTS = 9;

    // ������ά��������ʾԤԼ���
    char schedule[MAX_TIMESLOTS][7];

    // ��ʼ��ԤԼ�������
    for (int i = 0; i < MAX_TIMESLOTS; ++i)
    {
        for (int j = 0; j < 7; ++j)
        {
            schedule[i][j] = ' ';
        }
    }

    // ����ԤԼ��Ϣ����ԤԼ�������
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

    // ���ʵ���ұ�ź�ԤԼ���
    cout << endl;
    cout << WARNING_YELLOW << "ʵ���� " << INFO_BLUE << labNumber << WARNING_YELLOW << " ��ԤԼ��Ϣ���£�" << RESET << endl;
    cout << endl;
    cout << "����\t\t1\t2\t3\t4\t5\t6\t7" << endl;
    cout << "������������������������������������������������������������������������������������������������������������������������������������������������" << endl;

    for (int i = 0; i < MAX_TIMESLOTS; ++i)
    {
        cout << "ʱ���" << i + 1 << "\t\t";
        for (int j = 0; j < 7; ++j)
        {
            if (schedule[i][j] == ' ')
            {
                cout << "��ԤԼ\t";
            }
            else
            {
                cout << schedule[i][j] << "\t";
            }
        }
        cout << endl;
    }
    cout << "������������������������������������������������������������������������������������������������������������������������������������������������" << endl;
}

// ����ʵ���ҿα�
void exportLabSchedule(const Appointment appointments[], int appointmentCount, const Lab labs[], int labCount)
{
    // ÿ��ʱ�����9��ʱ���
    const int MAX_TIMESLOTS = 9;
    // ÿ��������7��ʱ���
    const int MAX_DAYS = 7;

    // �����ļ������
    ofstream outputFile("output.txt");

    // ����ÿ��ʵ����
    for (int labIndex = 0; labIndex < labCount; ++labIndex)
    {
        const Lab& lab = labs[labIndex];
        outputFile << "                                             ";
        outputFile << "ʵ����" << lab.labNumber << "�����ͣ�";
        outputFile << (lab.labType == HARDWARE ? "Ӳ��" : "���");
        outputFile << "����λ������" << lab.labSize << "���α�" << endl;
        outputFile << endl;

        // ������ά��������ʾ�α�
        string schedule[MAX_TIMESLOTS][MAX_DAYS];

        // ��ʼ���α�Ϊ��
        for (int i = 0; i < MAX_TIMESLOTS; ++i)
        {
            for (int j = 0; j < MAX_DAYS; ++j)
            {
                schedule[i][j] = "";
            }
        }

        // ���α�
        for (int appointmentIndex = 0; appointmentIndex < appointmentCount; ++appointmentIndex)
        {
            const Appointment& appointment = appointments[appointmentIndex];

            // ���ԤԼ��ʵ�����뵱ǰʵ������ͬ
            if (appointment.labNumber == lab.labNumber)
            {
                int startTime = appointment.startTime - 1;
                int endTime = appointment.endTime;

                // ����ԤԼ��ʱ���
                for (int j = startTime; j < endTime; ++j)
                {
                    int dayOfWeek = appointment.date % 7;
                    schedule[j][dayOfWeek] = appointment.lessonName;
                }
            }
        }

        // ����α��ļ�
        outputFile << "������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������" << endl;
        outputFile << "����\t\t1\t\t2\t\t3\t\t4\t\t5\t\t6\t\t7" << endl;

        for (int i = 0; i < MAX_TIMESLOTS; ++i)
        {
            outputFile << "ʱ���" << i + 1 << "\t\t";
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

// ��ӡ���˵�
void showmenu()
{
    cout << "������������������������������������������������������������" << WARNING_YELLOW << " ��ӭʹ��ʵ����ԤԼϵͳ! " << RESET << "��������������������������������������������������������������" << endl;
    cout << "                                                                  ��ǰ�汾:v1.2.1214 " << endl;
    cout << "                            1.   ��ʾ����ʵ���ҵ���Ϣ" << endl;
    cout << "                            2.       ԤԼʵ����" << endl;
    cout << "                            3.        ȡ��ԤԼ" << endl;
    cout << "                            4.    ��ʾ����ԤԼ��Ϣ" << endl;
    cout << "                            5. �����ڲ�ѯʵ����ԤԼ���" << endl;
    cout << "                            6. ��ʵ���ұ�Ų�ѯԤԼ���" << endl;
    cout << "                            7.   ����ʵ���ҿα��ļ�" << endl;
    cout << "                            0.        �˳�����" << endl;
    cout << endl;
    cout << "����������������������������������������������������������������������������������������������������������������������������������������������������������������������������" << endl;
    cout << endl;
    cout << INFO_BLUE << "[INFO]:���������ѡ��[0-4]:" << RESET;
    return;
}

// �����û�ѡ��
void choosechoice(int choice, Lab labs[], Appointment appointments[])
{
    switch (choice)
    {
    case 1:
    {
        cout << WARNING_YELLOW << "�������������������������������� ��ǰλ�ڣ�1.��ʾ����ʵ���ҵ���Ϣ ��������������������������������" << RESET << endl;
        cout << endl;
        int labCount;
        labCount = importLabInfo(labs, MAX_LAB);
        cout << endl;
        showLabInfo(labs, labCount);
        cout << endl;
        cout << INFO_BLUE << "[INFO]:�����������������..." << RESET << endl;
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
            cout << WARNING_YELLOW << "�������������������������������� ��ǰλ�ڣ�2.ԤԼʵ���� ��������������������������������" << RESET << endl;
            cout << endl;
            Reservation reservation;
            makeReservation(labs, MAX_LAB, reservation);
            cout << endl;
            cout << INFO_BLUE << "[INFO]:����ԤԼ?(Y/N)" << RESET;
            cin >> temp;
            system("cls");
        } while (temp == 'Y' || temp == 'y');
        break;
    }
    case 3:
    {
        cout << WARNING_YELLOW << "�������������������������������� ��ǰλ�ڣ�3.ȡ��ԤԼ ��������������������������������" << RESET << endl;
        cout << endl;
        int count = readAppointment(appointments, MAX_APPOINTMENTS);
        cancelAppointment(appointments, count);
        cout << endl;
        cout << INFO_BLUE << "[INFO]:�����������������..." << RESET << endl;
        cin.get();
        cin.get();
        system("cls");
        break;
    }
    case 4:
    {
        cout << WARNING_YELLOW << "�������������������������������� ��ǰλ�ڣ�4.��ʾ����ԤԼ��Ϣ ��������������������������������" << RESET << endl;
        cout << endl;
        int count = readAppointment(appointments, MAX_APPOINTMENTS);
        showAppointment(appointments, count);
        cout << endl;
        cout << INFO_BLUE << "[INFO]:�����������������..." << RESET << endl;
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
            cout << WARNING_YELLOW << "�������������������������������� ��ǰλ�ڣ�5. �����ڲ�ѯʵ����ԤԼ��� ��������������������������������" << RESET << endl;
            int date;
            cout << endl;
            cout << "[INFO]:������Ҫ��ѯ������(YYYMMDD): ";
            cin >> date;
            int appointmentCount = readAppointment(appointments, MAX_APPOINTMENTS);
            displayLabScheduleDate(appointments, appointmentCount, date);
            cout << endl;
            cout << INFO_BLUE << "[INFO]:������ѯ?(Y/N)" << RESET;
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
            cout << WARNING_YELLOW << "�������������������������������� ��ǰλ�ڣ�6. ��ʵ���ұ�Ų�ѯԤԼ��� ��������������������������������" << RESET << endl;
            cout << endl;
            int labindex;
            cout << "[INFO]:������Ҫ��ѯ��ʵ���ұ��(1-8): ";
            cin >> labindex;
            int appointmentCount = readAppointment(appointments, MAX_APPOINTMENTS);
            displayLabScheduleLab(appointments, appointmentCount, labindex);
            cout << endl;
            cout << INFO_BLUE << "[INFO]:������ѯ?(Y/N)" << RESET;
            cin >> temp;
            system("cls");
        } while (temp == 'Y' || temp == 'y');
        break;
    }
    case 7:
    {
        cout << WARNING_YELLOW << "�������������������������������� ��ǰλ�ڣ�7. ����ʵ���ҿα��ļ� ��������������������������������" << RESET << endl;
        cout << endl;
        int appointmentCount = readAppointment(appointments, MAX_APPOINTMENTS);
        exportLabSchedule(appointments, appointmentCount, labs, MAX_LAB);
        cout << "�ѳɹ�����α�output.txt��";
        cout << endl;
        cout << INFO_BLUE << "[INFO]:�����������������..." << RESET << endl;
        cin.get();
        cin.get();
        system("cls");
        break;
    }
    case 0:
    {
        cout << INFO_BLUE << "[INFO]:��ӭ�´�ʹ�ã��ټ���" << endl;
        MessageBox(NULL, L"��ӭ�´�ʹ�ã��ټ���", L"�˳�", MB_OK);
        return;
    }
    }
}

int main()
{
    // �������飬���ڴ洢ʵ������Ϣ
    Lab labs[MAX_LAB];
    // �������飬���ڴ洢ԤԼ��Ϣ
    Appointment appointments[MAX_APPOINTMENTS];

    // ��ȡʵ������Ϣ
    if (!importLabInfo(labs, MAX_LAB))
    {
        return 0;
    }
    Sleep(500);
    system("cls");

    // ����һ�����������ڴ洢�û������ѡ��
    int choice;
    // ѭ��ִ�У�ֱ���û�����0
    do
    {
        // ��ʾ�˵�
        showmenu();
        // ��ȡ�û������ѡ��
        cin >> choice;
        system("cls");
        // �����û������ѡ�����choosechoice����
        choosechoice(choice, labs, appointments);
    } while (choice != 0);
    return 0;
}
