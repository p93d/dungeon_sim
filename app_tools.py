from dataclasses import dataclass
from dash import dcc, html
import numpy as np
import pandas as pd
from threading import Thread



class_names = [
    'Assassin',
    'Brawler',
    'Cavalry',
    'Healer',
    'Hunter',
    'Knight',
    'Mage',
    'Priest',
    'Tank',
    'Warrior',
    'Wizard'    
]



@dataclass
class DungeonFighter:

    fighter_class: str
    max_hp: int
    health: int
    defense: int
    damage: int
    crit: float
    hit: int
    dodge: int
    fighter_pos: int
    block: float = 0.0
    dam_red: float = 0.0
    stun_rd: int = 0
    tank_rd: int = 0
    hit_counter: int = 0




def monster_stats(lvl):

    if lvl <= 600:
        scale_value = 0
    else:
        scale_value = sum([i for i in range(lvl-600, 0, -200)])

    stats = [
    400*lvl + 400*scale_value + 100,
    10*lvl + 10*scale_value + 20,
    40*lvl + 40*scale_value + 60,
    1.0,
    30*lvl + 30*scale_value + 50,
    30*lvl + 30*scale_value + 50,
    ]

    return stats



def stat_cost(points):

    return sum([i*10000 for i in range(points+1)])



def stat_value(points):

    out = []
    out.append(500 + 100*points[0]) # hp
    out.append(25 + 10*points[1]) # defense
    out.append(100 + 25*points[2]) # damage
    out.append(.0025*points[3]) # crit
    out.append(50 + 50*points[4]) # hit
    out.append(50 + 50*points[5]) # dodge

    return out





def sim_fight(_monsters, _fighters, num_sims=1, result=None, index=None):

    win_count = 0

    for sim in range(num_sims):    

        round_counter = 1
        active_fight = True

        combat_log = []

        monsters = []

        for c, monster in enumerate(_monsters):

            monsters.append(
                    DungeonFighter(
                    fighter_class='monster',
                    max_hp=monster[0],
                    health=monster[0],
                    defense=monster[1],
                    damage=monster[2],
                    crit=monster[3],
                    hit=monster[4],
                    dodge=monster[5],
                    fighter_pos=c+1
                ))


        fighters = []

        for c, fighter in enumerate(_fighters):

            fighters.append(
                    DungeonFighter(
                    fighter_class=fighter[0],
                    max_hp=fighter[1],
                    health=fighter[1],
                    defense=fighter[2],
                    damage=fighter[3],
                    crit=fighter[4],
                    hit=fighter[5],
                    dodge=fighter[6],
                    block=fighter[7],
                    dam_red=fighter[8],
                    fighter_pos=c+1
                )
            )

    

        while active_fight:

            # Fights end in a loss if they exceen 150 rounds
            if round_counter == 150:
                active_fight = False
                break

            # MONSTERS will attack first
            # could update this is in the future to
            # use HIT stat to determine order
            for monster in monsters:

                block_flag = False

                if monster.health <= 0:
                    continue

                # check if monster is stunned this round
                elif monster.stun_rd > 0:
                    combat_log.append(
                        html.H6(
                            f'Monster {monster.fighter_pos} did not attack - STUNNED',
                            className="text-warning"
                        )
                    )
                    monster.stun_rd-=1

                # otherwise determine which fighter to attack
                # and attack
                else:

                    # check for the first active fighter with > 0 hp
                    for fighter in fighters:
                        if fighter.health > 0:
                            active_fighter = fighter
                            break
                    # if none are found, end the fight
                    else:
                        active_fight = False
                        break

                    # HIT Chance for Monster
                    hit_pct = (monster.hit / (active_fighter.dodge + monster.hit))
                    
                    hit_draw = np.random.rand(1)[0]

                    # HIT
                    if hit_draw < hit_pct:

                        monster.hit_counter+=1

                        # every 10 hits is a crit
                        if monster.hit_counter % 10 == 0:
                            crit_modifier = monster.crit
                        else:
                            crit_modifier = 0

                        # defense subtracts from total damage
                        total_damage = monster.damage * (1 + crit_modifier)
                        net_damage = (total_damage - active_fighter.defense)
                        if net_damage < 0:
                            net_damage = 0


                        # Block Attempt
                        if np.random.rand(1)[0] < active_fighter.block:

                            # if the fighter is a Knight, we block 80% of damage
                            if active_fighter.fighter_class == 'Knight':
                                net_damage*=.2
                            # if it's not a knight, we block 40% of the damage
                            else:
                                net_damage*=.6

                        # unsuccessful block - Knight still blocks 40%
                        else:
                            if active_fighter.fighter_class == 'Knight':
                                net_damage*=.6
                        

                        # Check for Tank Ability
                        # If ability is active, add 50% damage reduction
                        #  if ability is INACTIVE, it has a 15% chance to proc
                        if active_fighter.fighter_class == 'Tank':

                            # If tank ability is active, add 50% to DR
                            if active_fighter.tank_rd > 0:

                                net_damage*=(1-(.5+active_fighter.dam_red))

                            # if ability is not active, see if the abiltiy activates
                            else:

                                if np.random.rand(1)[0] < .15:
                                    active_fighter.tank_rd = 3
                                    
                                    net_damage*=(1-(.5+active_fighter.dam_red))

                        else:
                            net_damage*=(1-active_fighter.dam_red)

                        # apply damage
                        if net_damage < active_fighter.health:
                            combat_log.append(
                                html.H6(
                                    f'Monster {monster.fighter_pos} attacked Fighter \
                                        {active_fighter.fighter_pos} for \
                                        {int(net_damage):,} damage \
                                        {" (CRIT)"if crit_modifier>0 else ""}',
                                    className="text-warning"
                                )
                            )
                            active_fighter.health-=net_damage
                        else:
                            combat_log.append(
                                html.H6(
                                    f'Monster {monster.fighter_pos} attacked Fighter \
                                        {active_fighter.fighter_pos} for \
                                        {int(active_fighter.health):,} damage - Fighter Killed\
                                        {" (CRIT)"if crit_modifier>0 else ""}',
                                    className="text-warning"
                                )
                            )
                            
                            active_fighter.health = 0

                    else:
                        combat_log.append(
                            html.H6(
                            f'Monster missed Fighter {active_fighter.fighter_pos}',
                            className="text-warning",
                            ) 
                        )


            # if the tank's ability is active, reduce
            # the amount of remaining rounds
            if active_fighter.tank_rd > 0:
                active_fighter.tank_rd-=1

            
            # Then let fighters attack
            for fighter in fighters:
                
                # Check if the fighter is alive
                if fighter.health > 0:

                    # If the fighter is a Priest they have
                    # a 10% chance to raise a dead teammate
                    #
                    # Then they attack as normal
                    if fighter.fighter_class == 'Priest':
                        if np.random.rand(1)[0] < .10:
                            
                            for _ftr in fighters:
                                if _ftr.health <= 0:
                                    _ftr.health = _ftr.max_hp

                                    combat_log.extend([
                                        f'Fighter {_ftr.fighter_pos} Resurrected by Priest',
                                        html.Br()
                                    ])

                                    break


                    if fighter.fighter_class == 'Knight':
                        combat_log.extend([
                            f"Fighter {fighter.fighter_pos} did not attack (cuz Knight lol)",
                            html.Br()
                        ])
                        
                        continue


                    elif fighter.fighter_class == 'Cavalry':

                        # Check which monster to attack
                        for monster in monsters:

                            if monster.health > 0:
                                active_monster = monster
                                break
                        else:
                            active_fight = False
                            win_count+=1
                            break

                        # HIT Chance for Fighter
                        hit_pct = (fighter.hit*2 / (active_monster.dodge + fighter.hit*2))
                        hit_draw = np.random.rand(1)[0]

                        # HIT
                        if hit_draw < hit_pct:
                            fighter.hit_counter+=1

                            # every 10 hits is a crit
                            if fighter.hit_counter % 10 == 0:
                                crit_modifier = fighter.crit
                            else:
                                crit_modifier = 0

                            # defense subtracts from total damage
                            total_damage = fighter.damage * (1 + crit_modifier)
                            net_damage = total_damage - active_monster.defense
                            
                            if net_damage < 0:
                                net_damage = 0

                            # apply damage
                            if net_damage < active_monster.health:
                                combat_log.extend([
                                    f'Fighter {fighter.fighter_pos} attacked Monster \
                                    {active_monster.fighter_pos} for {int(net_damage):,} damage',
                                    f'{" (CRIT)"if crit_modifier>0 else ""}',
                                    html.Br()
                                    ])
 
                                active_monster.health-=net_damage

                            else:

                                combat_log.extend([
                                    f'Fighter {fighter.fighter_pos} attacked Monster \
                                        {active_monster.fighter_pos} for {int(active_monster.health):,} \
                                        damage - Monster Killed',
                                    f'{" (CRIT)"if crit_modifier>0 else ""}',
                                    html.Br()
                                    ])
                                
                                active_monster.health = 0

                        else:
                            combat_log.extend([
                                f'Fighter {fighter.fighter_pos} missed (lmao)',
                                html.Br()
                            ])


                    elif fighter.fighter_class == 'Brawler':

                        # Check which monster to attack
                        for monster in monsters:

                            if monster.health > 0:
                                active_monster = monster
                                break
                        else:
                            active_fight = False
                            win_count+=1
                            break


                        # HIT Chance for Fighter
                        hit_pct = (fighter.hit / (active_monster.dodge + fighter.hit))
                        hit_draw = np.random.rand(1)[0]

                        # HIT
                        if hit_draw < hit_pct:
                            fighter.hit_counter+=1

                            # every 10 hits is a crit
                            if fighter.hit_counter % 10 == 0:
                                crit_modifier = fighter.crit
                            else:
                                crit_modifier = 0

                            # defense subtracts from total damage
                            total_damage = fighter.damage * (1 + crit_modifier)
                            net_damage = total_damage - active_monster.defense
                            

                            if net_damage < 0:
                                net_damage = 0
                        
                            # apply damage
                            if net_damage < active_monster.health:
                                combat_log.extend([
                                    f'Fighter {fighter.fighter_pos} attacked Monster \
                                    {active_monster.fighter_pos} for {int(net_damage):,} damage',
                                    f'{" (CRIT)"if crit_modifier>0 else ""}',
                                    html.Br()
                                    ])
 
                                active_monster.health-=net_damage

                            else:

                                combat_log.extend([
                                    f'Fighter {fighter.fighter_pos} attacked Monster \
                                        {active_monster.fighter_pos} for {int(active_monster.health):,} \
                                        damage - Monster Killed',
                                    f'{" (CRIT)"if crit_modifier>0 else ""}',
                                    html.Br()
                                    ])
                                
                                active_monster.health = 0
                        else:
                            combat_log.extend([
                                f'Fighter {fighter.fighter_pos} missed (lmao)',
                                html.Br()
                            ])

                        # brawler gets a 15% chance to attack twice
                        if np.random.rand(1)[0] < .15:
                            # Check which monster to attack
                            for monster in monsters:

                                if monster.health > 0:
                                    active_monster = monster
                                    break
                            else:
                                active_fight = False
                                win_count+=1
                                break


                            # HIT Chance for Fighter
                            hit_pct = (fighter.hit / (active_monster.dodge + fighter.hit))
                            hit_draw = np.random.rand(1)[0]

                            # HIT
                            if hit_draw < hit_pct:
                                fighter.hit_counter+=1

                                # every 10 hits is a crit
                                if fighter.hit_counter % 10 == 0:
                                    crit_modifier = fighter.crit
                                else:
                                    crit_modifier = 0

                                # defense subtracts from total damage
                                total_damage = fighter.damage * (1 + crit_modifier)
                                net_damage = total_damage - active_monster.defense
                                
                                if net_damage < 0:
                                    net_damage = 0
                            
                                # apply damage
                                if net_damage < active_monster.health:
                                    combat_log.extend([
                                        f'Fighter {fighter.fighter_pos} attacked Monster \
                                        {active_monster.fighter_pos} for {int(net_damage):,} damage',
                                        f'{" (CRIT)"if crit_modifier>0 else ""}',
                                        html.Br()
                                        ])
    
                                    active_monster.health-=net_damage

                                else:

                                    combat_log.extend([
                                        f'Fighter {fighter.fighter_pos} attacked Monster \
                                            {active_monster.fighter_pos} for {int(active_monster.health):,} \
                                            damage - Monster Killed',
                                        f'{" (CRIT)"if crit_modifier>0 else ""}',
                                        html.Br()
                                        ])
                                    
                                    active_monster.health = 0

                            else:
                                combat_log.extend([
                                    f'Fighter {fighter.fighter_pos} missed (lmao)',
                                    html.Br()
                                ])



                    elif fighter.fighter_class == 'Warrior':

                        # Check which monster to attack
                        for monster in monsters:

                            if monster.health > 0:
                                active_monster = monster
                                break
                        else:
                            active_fight = False
                            win_count+=1
                            break


                        # HIT Chance for Fighter
                        hit_pct = (fighter.hit / (active_monster.dodge + fighter.hit))
                        hit_draw = np.random.rand(1)[0]

                        # HIT
                        if hit_draw < hit_pct:
                            fighter.hit_counter+=1

                            # every 10 hits is a crit
                            if fighter.hit_counter % 10 == 0:
                                crit_modifier = fighter.crit
                            else:
                                crit_modifier = 0

                            # defense subtracts from total damage
                            total_damage = fighter.damage * (1 + crit_modifier)
                            net_damage = total_damage - active_monster.defense
                            
                            if net_damage < 0:
                                net_damage = 0
                        
                            # apply damage
                            if net_damage < active_monster.health:
                                combat_log.extend([
                                    f'Fighter {fighter.fighter_pos} attacked Monster \
                                    {active_monster.fighter_pos} for {int(net_damage):,} damage',
                                    f'{" (CRIT)"if crit_modifier>0 else ""}',
                                    html.Br()
                                    ])
 
                                active_monster.health-=net_damage

                            else:

                                combat_log.extend([
                                    f'Fighter {fighter.fighter_pos} attacked Monster \
                                        {active_monster.fighter_pos} for {int(active_monster.health):,} \
                                        damage - Monster Killed',
                                    f'{" (CRIT)"if crit_modifier>0 else ""}',
                                    html.Br()
                                    ])
                                
                                active_monster.health = 0

                            # warrior gets a 10% chance to stun enemy for 3 rounds
                            if np.random.rand(1)[0] < .10:
                                combat_log.extend([
                                    f'WARRIOR ABILITY ACTIVED - MONSTER \
                                        {active_monster.fighter_pos} STUNNED',
                                    html.Br()
                                ])

                                active_monster.stun_rd = 2

                        else:
                            combat_log.extend([
                                f'Fighter {fighter.fighter_pos} missed (lmao)',
                                html.Br()
                            ])
                                
                    

                    # Assassins prioritize attacking the second column first
                    elif fighter.fighter_class == 'Assassin':

                        assassin_attack_order = monsters[3:] + monsters[:3]

                        # Check which monster to attack
                        for monster in assassin_attack_order:

                            if monster.health > 0:
                                active_monster = monster
                                break
                        else:
                            active_fight = False
                            win_count+=1
                            break


                        # HIT Chance for Fighter
                        hit_pct = (fighter.hit / (active_monster.dodge + fighter.hit))
                        hit_draw = np.random.rand(1)[0]

                        # HIT
                        if hit_draw < hit_pct:
                            fighter.hit_counter+=1

                            # every 10 hits is a crit
                            if fighter.hit_counter % 10 == 0:
                                crit_modifier = fighter.crit
                            else:
                                crit_modifier = 0

                            # defense subtracts from total damage
                            total_damage = fighter.damage * (1 + crit_modifier)
                            net_damage = total_damage - active_monster.defense
                            

                            if net_damage < 0:
                                net_damage = 0
                        
                            # apply damage
                            if net_damage < active_monster.health:
                                combat_log.extend([
                                    f'Fighter {fighter.fighter_pos} attacked Monster \
                                    {active_monster.fighter_pos} for {int(net_damage):,} damage',
                                    f'{" (CRIT)"if crit_modifier>0 else ""}',
                                    html.Br()
                                    ])
 
                                active_monster.health-=net_damage

                            else:

                                combat_log.extend([
                                    f'Fighter {fighter.fighter_pos} attacked Monster \
                                        {active_monster.fighter_pos} for {int(active_monster.health):,} \
                                        damage - Monster Killed',
                                    f'{" (CRIT)"if crit_modifier>0 else ""}',
                                    html.Br()
                                    ])
                                
                                active_monster.health = 0

                        else:
                            combat_log.extend([
                                f'Fighter {fighter.fighter_pos} missed (lmao)',
                                html.Br()
                            ])



                    # hunters attack the active row for 75% damage
                    elif fighter.fighter_class == 'Hunter':

                        # Check which monster to attack
                        for c, monster in enumerate(monsters):

                            if monster.health > 0:
                                if c > 2:
                                    active_monsters = [monsters[c]]
                                else:
                                    active_monsters = [monsters[c], monsters[c+3]]
                                break
                        else:
                            active_fight = False
                            win_count+=1
                            break

                        for active_monster in active_monsters:

                            if active_monster.health > 0:

                                # HIT Chance for Fighter
                                hit_pct = (fighter.hit / (active_monster.dodge + fighter.hit))
                                hit_draw = np.random.rand(1)[0]

                                # HIT
                                if hit_draw < hit_pct:
                                    fighter.hit_counter+=1

                                    # every 10 hits is a crit
                                    if fighter.hit_counter % 10 == 0:
                                        crit_modifier = fighter.crit
                                    else:
                                        crit_modifier = 0

                                    # defense subtracts from total damage
                                    total_damage = fighter.damage * (1 + crit_modifier)
                                    total_damage*=.75

                                    net_damage = total_damage - active_monster.defense
                                    
                                    if net_damage < 0:
                                        net_damage = 0
                                
                                    # apply damage
                                    if net_damage < active_monster.health:
                                        combat_log.extend([
                                            f'Fighter {fighter.fighter_pos} attacked Monster \
                                            {active_monster.fighter_pos} for {int(net_damage):,} damage',
                                            f'{" (CRIT)"if crit_modifier>0 else ""}',
                                            html.Br()
                                            ])
        
                                        active_monster.health-=net_damage

                                    else:

                                        combat_log.extend([
                                            f'Fighter {fighter.fighter_pos} attacked Monster \
                                                {active_monster.fighter_pos} for {int(active_monster.health):,} \
                                                damage - Monster Killed',
                                            f'{" (CRIT)"if crit_modifier>0 else ""}',
                                            html.Br()
                                            ])
                                        
                                        active_monster.health = 0

                                else:
                                    combat_log.extend([
                                        f'Fighter {fighter.fighter_pos} missed (lmao)',
                                        html.Br()
                                    ])


                    # mages attack the active column for 50% damage
                    elif fighter.fighter_class == 'Mage':

                        # Check which monster to attack
                        for c, monster in enumerate(monsters):

                            if monster.health > 0:
                                if c > 2:
                                    active_monsters = monsters[3:]
                                else:
                                    active_monsters = monsters[:3]
                                break

                        else:
                            active_fight = False
                            win_count+=1
                            break

                        for active_monster in active_monsters:

                            if active_monster.health > 0:

                                # HIT Chance for Fighter
                                hit_pct = (fighter.hit / (active_monster.dodge + fighter.hit))
                                hit_draw = np.random.rand(1)[0]

                                # HIT
                                if hit_draw < hit_pct:
                                    fighter.hit_counter+=1

                                    # every 10 hits is a crit
                                    if fighter.hit_counter % 10 == 0:
                                        crit_modifier = fighter.crit
                                    else:
                                        crit_modifier = 0

                                    # defense subtracts from total damage
                                    total_damage = fighter.damage * (1 + crit_modifier)
                                    total_damage*=.5

                                    net_damage = total_damage - active_monster.defense
                                    
                                    if net_damage < 0:
                                        net_damage = 0
                                
                                    # apply damage
                                    if net_damage < active_monster.health:
                                        combat_log.extend([
                                            f'Fighter {fighter.fighter_pos} attacked Monster \
                                            {active_monster.fighter_pos} for {int(net_damage):,} damage',
                                            f'{" (CRIT)"if crit_modifier>0 else ""}',
                                            html.Br()
                                            ])
        
                                        active_monster.health-=net_damage

                                    else:

                                        combat_log.extend([
                                            f'Fighter {fighter.fighter_pos} attacked Monster \
                                                {active_monster.fighter_pos} for {int(active_monster.health):,} \
                                                damage - Monster Killed',
                                            f'{" (CRIT)"if crit_modifier>0 else ""}',
                                            html.Br()
                                            ])
                                        
                                        active_monster.health = 0

                                else:
                                    combat_log.extend([
                                        f'Fighter {fighter.fighter_pos} missed (lmao)',
                                        html.Br()
                                    ])


                    elif fighter.fighter_class == 'Healer':

                        fighter.hit_counter+=1

                        # every 10 hits is a crit
                        if fighter.hit_counter % 10 == 0:
                            crit_modifier = fighter.crit
                        else:
                            crit_modifier = 0


                        # figure out who to heal
                        for _fighter in fighters:

                            if 0 < _fighter.health < _fighter.max_hp:

                                total_damage = fighter.damage * (1 + crit_modifier)
                                net_damage = total_damage * .75
                                
                                _fighter.health+=net_damage

                                combat_log.extend([
                                        f'Healer {fighter.fighter_pos} healed Fighter \
                                            {_fighter.fighter_pos} for {int(net_damage):,} ',
                                        f'{" (CRIT)"if crit_modifier>0 else ""}',
                                        html.Br()
                                    ])

                                if _fighter.health > _fighter.max_hp:
                                    _fighter.health = _fighter.max_hp
                                    

                                break
                        
                    

                    # Wizard, Tank, Priest (No relevant attacking abilities)
                    else:

                        # Check which monster to attack
                        for monster in monsters:

                            if monster.health > 0:
                                active_monster = monster
                                break
                        else:
                            active_fight = False
                            win_count+=1
                            break


                        # HIT Chance for Fighter
                        hit_pct = (fighter.hit / (active_monster.dodge + fighter.hit))
                        hit_draw = np.random.rand(1)[0]

                        # HIT
                        if hit_draw < hit_pct:
                            fighter.hit_counter+=1

                            # every 10 hits is a crit
                            if fighter.hit_counter % 10 == 0:
                                crit_modifier = fighter.crit
                            else:
                                crit_modifier = 0

                            # defense subtracts from total damage
                            total_damage = fighter.damage * (1 + crit_modifier)
                            net_damage = total_damage - active_monster.defense
                            
                            if net_damage < 0:
                                net_damage = 0
                        
                            # apply damage
                            if net_damage < active_monster.health:
                                combat_log.extend([
                                    f'Fighter {fighter.fighter_pos} attacked Monster \
                                    {active_monster.fighter_pos} for {int(net_damage):,} damage',
                                    f'{" (CRIT)"if crit_modifier>0 else ""}',
                                    html.Br()
                                    ])

                                active_monster.health-=net_damage

                            else:

                                combat_log.extend([
                                    f'Fighter {fighter.fighter_pos} attacked Monster \
                                        {active_monster.fighter_pos} for {int(active_monster.health):,} \
                                        damage - Monster Killed',
                                    f'{" (CRIT)"if crit_modifier>0 else ""}',
                                    html.Br()
                                    ])
                                
                                active_monster.health = 0

                        else:
                            combat_log.extend([
                                f'Fighter {fighter.fighter_pos} missed (lmao)',
                                html.Br()
                            ])

            round_counter+=1



    if num_sims==1:

        if win_count == 1:
            combat_log.extend([
                html.Br(),
                html.Br(),
                f'You WON after {round_counter} rounds',
            ])
            
        else:
            combat_log.extend([
                html.Br(),
                html.Br(),
                f'You LOST after {round_counter} rounds',
            ])
        
        return combat_log

    else:
        # print(win_count)
        # result[index] = win_count

        return win_count

    