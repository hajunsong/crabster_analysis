QT -= gui

CONFIG += c++11 console
CONFIG -= app_bundle

SOURCES += \
    $$PWD/../src/main.cpp \
	$$PWD/../src/basebody.cpp \
	$$PWD/../src/subsystem.cpp \
	$$PWD/../src/simulation.cpp \

HEADERS += \
    $$PWD/../include/basebody.h \
	$$PWD/../include/subsystem.h \
	$$PWD/../include/simulation.h \
	$$PWD/../include/utils.h \

INCLUDEPATH += \
    $$PWD/../include \
	/usr/include/eigen3 \


