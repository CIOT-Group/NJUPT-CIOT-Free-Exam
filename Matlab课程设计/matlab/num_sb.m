% 主GUI文件，运行此文件打开GUI

function varargout = num_sb(varargin)
    gui_Singleton = 1;
    gui_State = struct('gui_Name',       mfilename, ...
                       'gui_Singleton',  gui_Singleton, ...
                       'gui_OpeningFcn', @num_sb_OpeningFcn, ...
                       'gui_OutputFcn',  @num_sb_OutputFcn, ...
                       'gui_LayoutFcn',  [] , ...
                       'gui_Callback',   []);
    if nargin && ischar(varargin{1})
        gui_State.gui_Callback = str2func(varargin{1});
    end
    
    if nargout
        [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
    else
        gui_mainfcn(gui_State, varargin{:});
    end

function num_sb_OpeningFcn(hObject, ~, handles, varargin)
    handles.output = hObject;
    clear global;clc
    set(gcf,'name','手写数字识别'); %修改GUI的界面名称
    guidata(hObject, handles);

function varargout = num_sb_OutputFcn(~, ~, handles) 
    varargout{1} = handles.output;

function pushbutton1_Callback(~, ~, handles)
    [Fnameh, Pnameh] = uigetfile({'*.*'; '*.jpg'; '*.png'}); % 弹出文件选择对话框，选择图像文件
    filename = [Pnameh, Fnameh]; % 合成文件的完整路径
    I = imread(filename);  % 读取选中的图像文件
    imshow(I);  % 显示读取的图像
    
    % 设置图像分割时的阈值，用于判断分割结果
    group_threshold = 120; % 可调的阈值，控制分组的分割效果
    [I_out, group] = grow(I, group_threshold);  % 调用grow函数进行图像分割，返回切片结果和分组信息
    % 加载已经训练好的LeNet-5模型
    load("Minist_LeNet5.mat", 'trainNet');  % 加载训练好的神经网络模型，包含手写数字识别网络
    % 初始化一个数组，存储每个切片的识别结果
    L = length(I_out);  % 获取切片的数量
    num = zeros(1, L);  % 初始化一个零数组，用来存储每个切片的识别结果
    for i = 1:L  % 对每个切片进行遍历
        I1 = I_out{i};% 获取当前的切片图像
        figure, imshow(I1); % 可视化当前的切片图像  
        % 对图像进行预处理，准备进行分类
        img = preprocessImage(I1);  % 调用图像预处理函数，将切片处理为网络可以接受的格式
        % 使用训练好的深度学习模型对图像进行分类
        result = classify(trainNet, img);  % 使用训练好的网络进行预测分类
        num(i) = double(result) - 1; % 将分类结果转换为数字标签（假设分类输出是字符类标签 '0'-'9'）
    end
    % 按照组进行拼接数字，并在每组之间插入空格
    result = "";  % 初始化结果字符串
    for g = 1:max([group.group_id])  % 遍历所有的分组
        group_digits = num([group.group_id] == g);  % 获取当前组的所有识别数字
        result = result + join(string(group_digits), '') + " ";  % 将当前组的数字拼接在一起，并加上空格
    end
    % 显示最终结果到界面上的文本框中
    set(handles.edit1, 'string', strtrim(result));  % 更新GUI中的文本框，显示识别结果


function edit1_CreateFcn(hObject, ~, ~)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

function axes1_CreateFcn(~, ~, ~)
    set(gca,'XColor',get(gca,'Color')) ;% 这两行代码功能：将坐标轴和坐标刻度转为白色
    set(gca,'YColor',get(gca,'Color'));
     
    set(gca,'XTickLabel',[]); % 这两行代码功能：去除坐标刻度
    set(gca,'YTickLabel',[]);

function img = preprocessImage(I)
    % 检查输入图像类型并处理
    if size(I, 3) == 3  % RGB 图像
        img = im2gray(I);  % 转灰度图（兼容性更高）
    else  % 灰度图
        img = I;  % 保持原样
    end
    
    % 继续图像的其他处理
    img = imresize(img, [28, 28]);        % 调整到28x28大小
    img = imbinarize(img, 0.5);           % 二值化
    img = imcomplement(img);              % 背景黑色，数字白色
    img = reshape(img, [28, 28, 1]);      % 调整维度以适配模型输入

