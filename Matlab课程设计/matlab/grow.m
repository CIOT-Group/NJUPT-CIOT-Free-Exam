function [I_out, group] = grow(I, group_threshold)
    I1 = rgb2gray(I);  % 转化为灰度图像
    I2 = edge(I1, 'canny', graythresh(I) * 0.7);  % 边缘检测
    I2 = imdilate(I2, ones(3, 3));
    I2 = imfill(I2, 'holes');
    I2 = imerode(I2, ones(3, 3));
    [x, ~] = find(I2 == 1);  % 找到数字的部分
    X = round(mean(x));  % 取对象的横向平均位置
    I3 = I2(X, :);  % 取出这一部分（相当于在原图像中选了一条横线）
    wz = find(I3 == 1);  % 找到对象的部分
    j = 0;  % 计数设置为0
    group = []; % 保存每个切片属于哪一组的数组
    current_group = 1; % 当前分组编号

    while ~isempty(wz)
        j = j + 1;  % 计数+1
        seed = [X, wz(1)];  % 更新种子点
        new = false(size(I2));  % 生成逻辑零数组保存之后的二值图像
        new(seed(1), seed(2)) = true;  % 种子点置一
        
        while true  % 开始生长
            for i = 1:size(seed, 1)  % 对每一种子点进行遍历
                new(seed(i, 1)-1:seed(i, 1)+1, seed(i, 2)-1:seed(i, 2)+1) = I2(seed(i, 1)-1:seed(i, 1)+1, seed(i, 2)-1:seed(i, 2)+1);
            end
            [x1, y1] = find(new == 1);  % 找到新的种子点
            seed1 = [x1, y1];  % 更新下一次遍历的种子点
            if length(seed) == length(seed1)  % 若本次和下次的种子数一致，则说明生长完成
                break;  % 退出
            end
            seed = seed1;  % 更新种子点
        end
        
        % 找到本次生长的对象
        pd = find(new(X, :) == 1);  
        wz = wz(length(pd) + 1:end);  % 将该对象从合集中去除
        [x, y] = find(new == 1);  % 得到本次对象的位置
        
        % 调整边界值（动态阈值）
        min_x = max(min(x) - 10, 1);
        max_x = min(max(x) + 10, size(I1, 1));
        min_y = max(min(y) - 10, 1);
        max_y = min(max(y) + 10, size(I1, 2));
        out = I1(min_x:max_x, min_y:max_y);  % 将其从原始灰度图像中取出来
        
        % 判断与上一切片是否属于同一组
        if j > 1
            prev_min_y = group(j-1).bounding_box(3);
            if min_y - prev_min_y <= group_threshold
                group(j).group_id = group(j-1).group_id;  % 同一组
            else
                current_group = current_group + 1;  % 新分组
                group(j).group_id = current_group;
            end
        else
            group(j).group_id = current_group;  % 第一个切片初始化为第一组
        end
        
        % 保存分组信息
        group(j).bounding_box = [min_x, max_x, min_y, max_y];
        group(j).image = out;
        
        % 存入输出数组
        I_out(j) = mat2cell(out, size(out, 1), size(out, 2));  % 将其放到cell数组中
    end

    if length(I_out) == 1  % 若输入的为单数字图像
        I_out = mat2cell(I1, size(I1, 1), size(I1, 2));  % 直接返回原始数字图像，因为这样精度更好一些
        group(1).group_id = 1;  % 单个图像的组号为1
    end
end



