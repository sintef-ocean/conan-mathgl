#include <QApplication>
#include <QMainWindow>
#include <QScrollArea>
#include <QTimer>
#include <mgl2/qmathgl.h>
#include <iostream>
int sample_1(mglGraph *gr){
  mglPoint pnt;
  pnt = mglPoint(2*mgl_rnd()-1,2*mgl_rnd()-1, 2*mgl_rnd());
  gr->Line(mglPoint(0,0,0),mglPoint(1, 1,1));
  return 0;
}

int main(int argc,char **argv)
{
  QApplication a(argc,argv);
  QMainWindow *Wnd = new QMainWindow;
  Wnd->resize(810,610);  // for fill up the QMGL, menu and toolbars
  Wnd->setWindowTitle("QMathGL sample");
  // here I allow to scroll QMathGL -- the case
  // then user want to prepare huge picture
  QScrollArea *scroll = new QScrollArea(Wnd);

  // Create and setup QMathGL
  QMathGL *QMGL = new QMathGL(Wnd);
  //QMGL->setPopup(popup); // if you want to setup popup menu for QMGL
  QMGL->setDraw(sample_1);
  // or use QMGL->setDraw(foo); for instance of class Foo:public mglDraw
  QMGL->update();

  // continue other setup (menu, toolbar and so on)
  scroll->setWidget(QMGL);
  Wnd->setCentralWidget(scroll);
  Wnd->show();

  QTimer *tim = new QTimer();
  QTimer::singleShot(10, &a, SLOT(quit()));

  std::cout << "Testing QMathGL Qt widget" << std::endl;

  return a.exec();
}
