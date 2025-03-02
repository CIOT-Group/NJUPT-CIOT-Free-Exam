% ��GUI�ļ������д��ļ���GUI

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
    set(gcf,'name','��д����ʶ��'); %�޸�GUI�Ľ�������
    guidata(hObject, handles);

function varargout = num_sb_OutputFcn(~, ~, handles) 
    varargout{1} = handles.output;

function pushbutton1_Callback(~, ~, handles)
    [Fnameh, Pnameh] = uigetfile({'*.*'; '*.jpg'; '*.png'}); % �����ļ�ѡ��Ի���ѡ��ͼ���ļ�
    filename = [Pnameh, Fnameh]; % �ϳ��ļ�������·��
    I = imread(filename);  % ��ȡѡ�е�ͼ���ļ�
    imshow(I);  % ��ʾ��ȡ��ͼ��
    
    % ����ͼ��ָ�ʱ����ֵ�������жϷָ���
    group_threshold = 120; % �ɵ�����ֵ�����Ʒ���ķָ�Ч��
    [I_out, group] = grow(I, group_threshold);  % ����grow��������ͼ��ָ������Ƭ����ͷ�����Ϣ
    % �����Ѿ�ѵ���õ�LeNet-5ģ��
    load("Minist_LeNet5.mat", 'trainNet');  % ����ѵ���õ�������ģ�ͣ�������д����ʶ������
    % ��ʼ��һ�����飬�洢ÿ����Ƭ��ʶ����
    L = length(I_out);  % ��ȡ��Ƭ������
    num = zeros(1, L);  % ��ʼ��һ�������飬�����洢ÿ����Ƭ��ʶ����
    for i = 1:L  % ��ÿ����Ƭ���б���
        I1 = I_out{i};% ��ȡ��ǰ����Ƭͼ��
        figure, imshow(I1); % ���ӻ���ǰ����Ƭͼ��  
        % ��ͼ�����Ԥ����׼�����з���
        img = preprocessImage(I1);  % ����ͼ��Ԥ������������Ƭ����Ϊ������Խ��ܵĸ�ʽ
        % ʹ��ѵ���õ����ѧϰģ�Ͷ�ͼ����з���
        result = classify(trainNet, img);  % ʹ��ѵ���õ��������Ԥ�����
        num(i) = double(result) - 1; % ��������ת��Ϊ���ֱ�ǩ���������������ַ����ǩ '0'-'9'��
    end
    % ���������ƴ�����֣�����ÿ��֮�����ո�
    result = "";  % ��ʼ������ַ���
    for g = 1:max([group.group_id])  % �������еķ���
        group_digits = num([group.group_id] == g);  % ��ȡ��ǰ�������ʶ������
        result = result + join(string(group_digits), '') + " ";  % ����ǰ�������ƴ����һ�𣬲����Ͽո�
    end
    % ��ʾ���ս���������ϵ��ı�����
    set(handles.edit1, 'string', strtrim(result));  % ����GUI�е��ı�����ʾʶ����


function edit1_CreateFcn(hObject, ~, ~)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end

function axes1_CreateFcn(~, ~, ~)
    set(gca,'XColor',get(gca,'Color')) ;% �����д��빦�ܣ��������������̶�תΪ��ɫ
    set(gca,'YColor',get(gca,'Color'));
     
    set(gca,'XTickLabel',[]); % �����д��빦�ܣ�ȥ������̶�
    set(gca,'YTickLabel',[]);

function img = preprocessImage(I)
    % �������ͼ�����Ͳ�����
    if size(I, 3) == 3  % RGB ͼ��
        img = im2gray(I);  % ת�Ҷ�ͼ�������Ը��ߣ�
    else  % �Ҷ�ͼ
        img = I;  % ����ԭ��
    end
    
    % ����ͼ�����������
    img = imresize(img, [28, 28]);        % ������28x28��С
    img = imbinarize(img, 0.5);           % ��ֵ��
    img = imcomplement(img);              % ������ɫ�����ְ�ɫ
    img = reshape(img, [28, 28, 1]);      % ����ά��������ģ������

