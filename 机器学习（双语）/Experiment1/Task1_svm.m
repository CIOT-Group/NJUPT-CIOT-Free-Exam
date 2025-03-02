clear;
addpath(genpath('.\libsvm-3.18'));
%# Fisher Iris dataset
load iris
[~,~,labels] = unique(species);   %# labels: 1/2/3
% data = zscore(meas);              %# scale features
data = meas;
numInst = size(data,1);
numLabels = max(labels);

%# split training/testing
idx = randperm(numInst);
numTrain = 100; numTest = numInst - numTrain;
trainData = data(idx(1:numTrain),:);  testData = data(idx(numTrain+1:end),:);
mean_train=mean(trainData);
std_train=std(trainData);
trainData=(trainData-ones(size(trainData,1),1)*mean_train)./(ones(size(trainData,1),1)*std_train);
testData=(testData-ones(size(testData,1),1)*mean_train)./(ones(size(testData,1),1)*std_train);

trainLabel = labels(idx(1:numTrain)); testLabel = labels(idx(numTrain+1:end));

%# train one-against-all models
model = cell(numLabels,1);
for k=1:numLabels
    model{k} = svmtrain(double(trainLabel==k), trainData, '-c 1 -g 0.2 -b 1');
end

%# get probability estimates of test instances using each model
prob = zeros(numTest,numLabels);
for k=1:numLabels
    [~,~,p] = svmpredict(double(testLabel==k), testData, model{k}, '-b 1');
    prob(:,k) = p(:,model{k}.Label==1);    %# probability of class==k
end

%# predict the class with the highest probability
[~,pred] = max(prob,[],2);
acc = sum(pred == testLabel) ./ numel(testLabel)    %# accuracy
C = confusionmat(testLabel, pred)                   %# confusion matrix
