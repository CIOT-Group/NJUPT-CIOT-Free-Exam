function GJ=chuli(I)
I1=edge(I,'canny',graythresh(I)*0.7);   %边缘检测
% subplot(2,2,1),imshow(I1),title('边缘检测后图像')
s=ones(2,2);    %方形模板
BWsdil = imdilate(I1,s);    %膨胀
BWs=imfill(BWsdil, 'holes');    %孔洞填充
% subplot(2,2,2),imshow(BWs),title('孔洞填充后图像')
GJ = imerode(BWs,s);   %腐蚀
% subplot(2,2,3),imshow(GJ),title('闭运算后图像')
[x,y]=find(GJ==1);   %找到数字部分
GJ=GJ(min(x):max(x),min(y):max(y));    %将数字部分提取出来
% subplot(2,2,4),imshow(GJ),title('大小处理后的图像')
end