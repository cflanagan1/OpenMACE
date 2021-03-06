#ifndef SPATIAL_ACTION_FACTORY_H
#define SPATIAL_ACTION_FACTORY_H

#include "mace.h"

#include "spatial_components.h"

namespace CommandItem {

class SpatialActionFactory
{
public:
   SpatialActionFactory() = default;

public:
   static AbstractSpatialActionPtr constructFromGoToCommand(const mace_command_goto_t &msg)
   {
       switch (static_cast<COMMANDITEM>(msg.action)) {
       case COMMANDITEM::CI_NAV_LOITER_TIME:
       {
            SpatialLoiter_TimePtr action = std::make_shared<SpatialLoiter_Time>();
            action->updateFromGoToCommand(msg);
            return action;
           break;
       }
       case COMMANDITEM::CI_NAV_LOITER_TURNS:
       {
            SpatialLoiter_TurnsPtr action = std::make_shared<SpatialLoiter_Turns>();
            action->updateFromGoToCommand(msg);
            return action;
           break;
       }
       case COMMANDITEM::CI_NAV_LOITER_UNLIM:
       {
            SpatialLoiter_UnlimitedPtr action = std::make_shared<SpatialLoiter_Unlimited>();
            action->updateFromGoToCommand(msg);
            return action;
           break;
       }
       case COMMANDITEM::CI_NAV_WAYPOINT:
       {
            SpatialWaypointPtr action = std::make_shared<SpatialWaypoint>();
            action->updateFromGoToCommand(msg);
            return action;
           break;
       }
       default:
           break;
       }
   }
};

} //end of namespace CommandItem
#endif // SPATIAL_ACTION_FACTORY_H
