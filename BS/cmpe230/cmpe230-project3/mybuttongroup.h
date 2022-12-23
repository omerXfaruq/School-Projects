#ifndef MYBUTTONGROUP_H
#define MYBUTTONGROUP_H

#include <QApplication>
#include <QPushButton>
#include <QButtonGroup>
#include <QLCDNumber>
#include <QVBoxLayout>
#include <QGridLayout>
#include <random>
#include <iostream>
#include <QDebug>
#include <windows.h>
#include <QDialog>
#include <QtMath>
#include <QRandomGenerator>
#include <QTimer>
#include <QLabel>
#include <QTextBrowser>



class MyButtonGroup: public QVBoxLayout
{
    Q_OBJECT
public:
    int status=0;
    const QSize TEXT_SIZE = QSize(60, 20);

    QTextBrowser *pairsShow=new QTextBrowser();
    QTextBrowser *triesShow=new QTextBrowser();


    QString letters[12]={"a","b","c","d","e","f","g","h","j","k","l","m"};

    bool buttonDone[24]={false,false,false,false,false,false,false,false,false,false,false,
                         false,false,false,false,false,false,false,false,false,false,false,false,false};
    int lastButton1=-1;
    int lastButton2=-1;
    QWidget       window ;
    QButtonGroup  buttongroup ;
    QPushButton  *button[24]  ;
    QGridLayout   glayout ;
    QLCDNumber    disp ;
    QString       s ;



    int* values;

    int pairs=0;
    int tries=0;

    int* randomizers();
    MyButtonGroup();

private slots:
    void compares();
    void changeButtonText(int x);
    void reset();



};
#endif // MYBUTTONGROUP_H
