#include "mybuttongroup.h"

int* MyButtonGroup::randomizers(){
    int set[24]={0,1,2,3,4,5,6,7,8,9,10,11,0,1,2,3,4,5,6,7,8,9,10,11};
    int* randomNumbers=new int[24];

    for (int i=0;i<24;i++){
        int random=qFabs(QRandomGenerator::global()->generate()%(24-i));
        int selectedNumber=set[random];
        int memory=set[23-i];            //Exchange items with last number, for not picking that number again
        set[23-i]=selectedNumber;
        set[random]=memory;
        randomNumbers[i]=selectedNumber;
    }
    return randomNumbers;
}


MyButtonGroup::MyButtonGroup():QVBoxLayout()
{

    pairsShow->setText("0");
    triesShow->setText("0");

    pairsShow->setMaximumSize(TEXT_SIZE);
    triesShow->setMaximumSize(TEXT_SIZE);

    QWidget *window= new QWidget;
    QVBoxLayout *mainLayout= new QVBoxLayout;
    QHBoxLayout *infoRow=new QHBoxLayout;
    QLabel *label = new QLabel;
    label->setText("Pairs");
    infoRow->addWidget(label);

    infoRow->addWidget(pairsShow);

    QPushButton *resetButton=new QPushButton("RESET");

    QLabel *label2 = new QLabel;
    label2->setText("Tries");
    infoRow->addWidget(label2);

    infoRow->addWidget(triesShow);

    infoRow->addWidget(resetButton);


    //infoRow->addWidget(showFails);

    values=randomizers();



    //disp.setSegmentStyle(QLCDNumber::Flat) ;
    //glayout.addWidget(&disp,0,0,1,-1);
    for(int i=0 ; i < 4 ; i++) {
        for(int j=0 ; j < 6 ; j++) {
            button[6*i+j] = new QPushButton("x");
            glayout.addWidget(button[6*i+j],i+1,j);

            buttongroup.addButton(button[6*i+j],(6*i+j));
        }
    }
    QObject::connect(&buttongroup, SIGNAL(buttonClicked(int)),
                     this, SLOT(changeButtonText(int)));


    QObject::connect(resetButton,SIGNAL(clicked()), this,SLOT(reset())); //needs work
    //values[buttonNo1%12]==values[buttonNo2%12];
    //letters[values[int%12]]


    mainLayout->addLayout(infoRow);
    mainLayout->addLayout(&glayout);
    window->setLayout(mainLayout); //will this work in main or lets make a function for this?
    window->show();              //will this work in main or lets make a function for this?
    //return app.exec(); will this work in main or lets make a function for this?


}

void MyButtonGroup::changeButtonText(int x){
    if(buttonDone[x]){
        return;
    }

    button[x]->setText(letters[values[x]]);



    if(status==0){

        lastButton1=x;
        status++;


    }
    else if(status==1){

        lastButton2=x;

        QTimer::singleShot(350, this, SLOT(compares()));//Waits between buttons


    }

}

void MyButtonGroup::compares(){
    if(lastButton1 != lastButton2 && values[lastButton1]==values[lastButton2]){
        button[lastButton1]->setText(" ");
        button[lastButton2]->setText(" ");

        buttonDone[lastButton1]=true;
        buttonDone[lastButton2]=true;

        pairs++;
        QString str=QString::number(pairs);
        pairsShow->setText(str);

    }
    else{

        button[lastButton1]->setText("x");
        button[lastButton2]->setText("x");
    }

    tries++;
    QString str=QString::number(tries);
    triesShow->setText(str);

    status=0;
    lastButton1=-1;
    lastButton2=-1;
}
void MyButtonGroup::reset(){
    values=randomizers();

    for(int i=0;i<24;i++){
        buttonDone[i]=false;
    }

    for (int i=0;i<24;i++) {
        button[i]->setText("x");
    }
    pairs=0;//       for display

    QString str=QString::number(pairs);
    pairsShow->setText(str);

    tries=0;//       for display

    str=QString::number(tries);
    triesShow->setText(str);

}


