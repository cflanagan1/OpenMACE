#ifndef MODULE_EXTERNAL_LINK_OFFSET_GLOBAL_H
#define MODULE_EXTERNAL_LINK_OFFSET_GLOBAL_H

#include <QtCore/qglobal.h>

#if defined(MODULE_EXTERNAL_LINK_OFFSET_LIBRARY)
#  define MODULE_EXTERNAL_LINK_OFFSETSHARED_EXPORT Q_DECL_EXPORT
#else
#  define MODULE_EXTERNAL_LINK_OFFSETSHARED_EXPORT Q_DECL_IMPORT
#endif

#endif // MODULE_EXTERNAL_LINK_OFFSET_GLOBAL_H
