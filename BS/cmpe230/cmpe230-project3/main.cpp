#include <QApplication>
#include <iostream>
#include <mybuttongroup.h>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    MyButtonGroup *mygroup= new MyButtonGroup();

    return app.exec();
}
