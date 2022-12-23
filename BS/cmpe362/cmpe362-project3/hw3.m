blurFilter=[ 1/9 1/9 1/9 ; 1/9 1/9 1/9 ; 1/9 1/9 1/9 ];
sharpenFilter=[ 0 -1 0 ; -1 5 -1 ; 0 -1 0];
edgeHighlightFilter=[-1 -1 -1 ; -1 8 -1 ; -1 -1 -1];
embossFilter=[-2 -1 0 ; -1 1 1 ; 0 1 2];

image=imread("image.png");
image= imresize(image, [512 512]);


%Zero padding
zeroPadded=zeros(514,514,3);
zeroPadded(2:513,2:513,:)=image;

%Convolution
blurredImage=imageConv(zeroPadded,blurFilter);
sharpenedImage=imageConv(zeroPadded,sharpenFilter);
edgesHighlightedImage=imageConv(zeroPadded,edgeHighlightFilter);
embossedImage=imageConv(zeroPadded,embossFilter);

%Data type conversion and image writing
myImageWrite(blurredImage,"1blur.png");
myImageWrite(sharpenedImage,"2sharpened.png");
myImageWrite(edgesHighlightedImage,"3edgeHighlight.png");
myImageWrite( embossedImage,"4embossed.png");

%%%Functions%%%

function [output] = flipUpDownAndLeftRight(matrix)
matrixSize=size(matrix);
output=zeros(matrixSize);
output1=zeros(matrixSize);

%Row based flip
for i=1:matrixSize(1)
    for j=1:matrixSize(2)
        output1(i,j)=matrix(matrixSize(1)-i+1,j);
    end
end
%Column based flip
for i=1:matrixSize(1)
    for j=1:matrixSize(2)
        output(i,j)=output1(i,matrixSize(2)-j+1);
    end
end
end

%3x3 matrix multiplication and addition
function [result] = localConv(matrix1, matrix2)

%This function does local multiplication and addition on 3x3 arrays

result=matrix1.*matrix2;
result=sum(result,'all');

end

%Data type conversion, and image writing
function [] = myImageWrite(input,path)
input=uint8(input);
imwrite(input,path);
end

%Convolution operation on whole image matrix
function [output] = imageConv(matrix1,matrix2)

matrix2=flipUpDownAndLeftRight(matrix2);
output=zeros(512,512,3);
for i=2:513
    for j=2:513
        for z=1:3
            littleMatrix1=matrix1(i-1:i+1,j-1:j+1,z);
            output(i-1,j-1,z)=localConv(littleMatrix1,matrix2);
        end 
    end
end
end
