function GJ=chuli(I)
I1=edge(I,'canny',graythresh(I)*0.7);   %��Ե���
% subplot(2,2,1),imshow(I1),title('��Ե����ͼ��')
s=ones(2,2);    %����ģ��
BWsdil = imdilate(I1,s);    %����
BWs=imfill(BWsdil, 'holes');    %�׶����
% subplot(2,2,2),imshow(BWs),title('�׶�����ͼ��')
GJ = imerode(BWs,s);   %��ʴ
% subplot(2,2,3),imshow(GJ),title('�������ͼ��')
[x,y]=find(GJ==1);   %�ҵ����ֲ���
GJ=GJ(min(x):max(x),min(y):max(y));    %�����ֲ�����ȡ����
% subplot(2,2,4),imshow(GJ),title('��С������ͼ��')
end