#ifndef COMMAND_GOTO_H
#define COMMAND_GOTO_H

#include "common/common.h"
#include "common/class_forward.h"

#include "data_generic_command_item/command_item_type.h"
#include "data_generic_command_item/abstract_command_item.h"

#include "../spatial_items/spatial_components.h"
#include "../spatial_items/spatial_action_factory.h"

namespace CommandItem {

MACE_CLASS_FORWARD(CommandGoTo);

class CommandGoTo : public AbstractCommandItem
{
public:
    /**
     * @brief getCommandType
     * @return
     */
    COMMANDITEM getCommandType() const override;

    /**
     * @brief getDescription
     * @return
     */
    std::string getDescription() const override;

    /**
     * @brief hasSpatialInfluence
     * @return
     */
    bool hasSpatialInfluence() const override;

    /**
     * @brief getClone
     * @return
     */
    std::shared_ptr<AbstractCommandItem> getClone() const override;

    /**
     * @brief getClone
     * @param state
     */
    void getClone(std::shared_ptr<AbstractCommandItem> &command) const override;

public:
    CommandGoTo();
    CommandGoTo(const AbstractSpatialActionPtr cmd);
    CommandGoTo(const CommandGoTo &obj);
    CommandGoTo(const int &systemOrigin, const int &systemTarget);

public:
    void setSpatialCommand(const AbstractSpatialActionPtr cmd)
    {
        m_SpatialAction = cmd;
    }

    AbstractSpatialActionPtr getSpatialCommand() const{
        return m_SpatialAction;
    }

    void updateFromGoToCommand(const mace_command_goto_t &msg)
    {
        if(m_SpatialAction == nullptr)
        {
            m_SpatialAction = CommandItem::SpatialActionFactory::constructFromGoToCommand(msg);
        }
        else
        {
            m_SpatialAction->updateFromGoToCommand(msg);
        }
    }

public:
    void operator = (const CommandGoTo &rhs)
    {
        AbstractCommandItem::operator =(rhs);
        this->m_SpatialAction = rhs.m_SpatialAction;
    }

    bool operator == (const CommandGoTo &rhs) {
        if(!AbstractCommandItem::operator ==(rhs))
        {
            return false;
        }

        if(this->m_SpatialAction != rhs.m_SpatialAction){
            return false;
        }

        return true;
    }

    bool operator != (const CommandGoTo &rhs) {
        return !(*this == rhs);
    }

    friend std::ostream &operator<<(std::ostream &out, const CommandGoTo &obj)
    {
//        out<<"Command Change Mode( Mode: "<<obj.vehicleMode<<")";
        return out;
    }

private:
    AbstractSpatialActionPtr m_SpatialAction;

};

} //end of namespace MissionItem

#endif // COMMAND_GOTO_H
