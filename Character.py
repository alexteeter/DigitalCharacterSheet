import configparser
import os
import math
import sys
import logging

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

global path
path = os.getcwd()

class Character:
    def __init__(self, level: int, profenciency: int, armorClass: int, strength: int, dex: int, constitution: int, intelligence: int, wisdom: int, charisma: int, hpMax: int, gold: float, name = None, race = None, subrace = None, charClass = None, hitDice = None, hit_die = ''):
        #self.weapons = self.Weapon()
        self.name = name
        self.race = race
        self.subrace = subrace
        self.languages = []
        self.charClass = charClass
        self.level = level
        self.prof = profenciency
        self.armorClass = armorClass
        self.strength = strength
        self.dex = dex
        self.con = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.hpMax = hpMax
        self.hpCurrent = hpMax
        self.gold = gold
        self.hitDice = hitDice
        self.currentHitDice = self.hitDice
        self.hit_die = hit_die
        self.equipment = []
        self.actions = []
        self.feats = []
        self.spells = []
        self.weapons = []
        self.inspiration = False
        self.isDown = False
        self.proficiencies = []
        self.pools = []
        self.spell_slots = {}
        self.current_spell_slots = self.spell_slots
        self.initiative_bonus = 0

    def mod(self, stat):
        mod = math.floor((int(stat)-10)/2)
        return mod
    def get_str_mod(self):
        self.strMod = self.mod(self.strength)
        return self.strMod
    def get_dex_mod(self):
        self.dexMod = self.mod(self.dex)
        return self.dexMod
    def get_con_mod(self):
        self.conMod = self.mod(self.con)
        return self.conMod
    def get_int_mod(self):
        self.intMod = self.mod(self.intelligence)
        return self.intMod
    def get_wis_mod(self):
        self.wisMod = self.mod(self.wisdom)
        return self.wisMod
    def get_cha_mod(self):
        self.chaMod = self.mod(self.charisma)
        return self.chaMod
    def get_passive_perception(self):
        self.passivePerception = 10+self.get_perception()
        return self.passivePerception     
    def get_initiative(self):
        self.initiative = int(self.get_dex_mod()) + int(self.initiative_bonus)
        return self.initiative
    
    def get_str_save(self):
        self.strSave = self.get_str_mod()
        if 'strength' in self.proficiencies:
            self.strSave += int(self.prof)
        return self.strSave
    def get_dex_save(self):
        self.dexSave = self.get_dex_mod()
        if 'dex' in self.proficiencies:
            self.dexSave += int(self.prof)
        return self.dexSave
    def get_con_save(self):
        self.conSave = self.get_con_mod()
        if 'con' in self.proficiencies or 'constitution' in self.proficiencies:
            self.conSave += int(self.prof)
        return self.conSave
    def get_int_save(self):
        self.intSave = self.get_int_mod()
        if 'intelligence' in self.proficiencies:
            self.intSave += int(self.prof)
        return self.intSave
    def get_wis_save(self):
        wisSave = self.get_wis_mod()
        if 'wisdom' in self.proficiencies:
            wisSave = int(wisSave) + int(self.prof)
        return wisSave
    def get_cha_save(self):
        self.chaSave = self.get_cha_mod()
        if 'charisma' in self.proficiencies:
            self.chaSave += int(self.prof)
        return self.chaSave

    def get_acrobatics(self):
        self.acrobatics = self.get_dex_mod()
        if 'acrobatics' in self.proficiencies:
            self.acrobatics += int(self.prof)
        return self.acrobatics
    def get_athletics(self):
        self.athletics = self.get_str_mod()
        if 'athletics' in self.proficiencies:
            self.athletics += int(self.prof)
        return self.athletics
    def get_animal_handling(self):
        self.animalHandling = self.get_wis_mod()
        if 'animal handling' in self.proficiencies:
            self.animalHandling += int(self.prof)
        return self.animalHandling
    def get_arcana(self):
        self.arcana = self.get_int_mod()
        if 'arcana' in self.proficiencies:
            self.arcana += int(self.prof)
        return self.arcana
    def get_deception(self):
        self.deception = self.get_cha_mod()
        if 'deception' in self.proficiencies:
            self.deception += int(self.prof)
        return self.deception
    def get_history(self):
        self.history = self.get_int_mod()
        if 'history' in self.proficiencies:
            self.history += int(self.prof)
        return self.history
    def get_insight(self):
        self.insight = self.get_wis_mod()
        if 'insight' in self.proficiencies:
            self.insight += int(self.prof)
        return self.insight
    def get_investigation(self):
        self.investigation = self.get_int_mod()
        if 'investigation' in self.proficiencies:
            self.investigation += int(self.prof)
        return self.investigation
    def get_intimidation(self):
        self.intimidation = self.get_cha_mod()
        if 'intimidation' in self.proficiencies:
            self.intimidation += int(self.prof)
        return self.intimidation   
    def get_medicine(self):
        self.medicine = self.get_wis_mod()
        if 'medicine' in self.proficiencies:
            self.medicine += int(self.prof)
        return self.medicine 
    def get_nature(self):
        self.nature = self.get_int_mod()
        if 'nature' in self.proficiencies:
            self.nature += int(self.prof)
        return self.nature
    def get_perception(self):
        self.perception = self.get_wis_mod()
        if 'perception' in self.proficiencies:
            self.perception += int(self.prof)
        return self.perception
    def get_performance(self):
        self.performance = self.get_cha_mod()
        if 'performance' in self.proficiencies:
            self.performance += int(self.prof)
        return self.performance
    def get_persuasion(self):
        self.persuasion = self.get_cha_mod()
        if 'persuasion' in self.proficiencies:
            self.persuasion += int(self.prof)
        return self.persuasion
    def get_religion(self):
        self.religion = self.get_int_mod()
        if 'religion' in self.proficiencies:
            self.religion += int(self.prof)
        return self.religion
    def get_sleight_of_hand(self):
        self.sleightOfHand = self.get_dex_mod()
        if 'sleight of hand' in self.proficiencies:
            self.sleightOfHand += int(self.prof)
        return self.sleightOfHand
    def get_stealth(self):
        self.stealth = self.get_dex_mod()
        if 'stealth' in self.proficiencies:
            self.stealth += int(self.prof)
        return self.stealth
    def get_survival(self):
        self.survival = self.get_wis_mod()
        if 'survival' in self.proficiencies:
            self.survival += int(self.prof)
        return self.survival
     
    def set_name(self, name):
        self.name = name
    def set_race(self, race):
        self.race = race
    def set_subrace(self, subrace):
        self.subrace = subrace
    def add_language(self, language):
        self.languages.append(language)
    def del_language(self, language):
        self.languages.remove(language)
    def set_charClass(self, charClass):
        self.charClass = charClass
    def set_level(self, level):
        self.level = level
    def set_prof(self, prof):
        self.prof = prof
    def set_insp(self, insp):
        self.insp = insp
    def set_armorClass(self, armorClass):
        self.armorClass = armorClass
    def set_strength(self, strength):
        self.strength = strength
    def set_dex(self, dex):
        self.dex = dex
    def set_con(self, con):
        self.con = con
    def set_intelligence(self, intelligence):
        self.intelligence = intelligence
    def set_wisdom(self, wisdom):
        self.wisdom = wisdom
    def set_charisma(self, charisma):
        self.charisma = charisma
    def set_hpMax(self, hpMax):
        self.hpMax = hpMax
    def set_gold(self, gold):
        self.gold = gold
    def add_gold(self, gold):
        self.gold = float(self.gold) + float(gold)
    def spend_gold(self, gold):
        self.gold = float(self.gold) - float(gold)
        if self.gold < 0:
            print('Negative gold value!')
    def add_action(self, action):
        self.actions.append(vars(action))
    def del_action(self, action):
        self.actions.remove(action)
    def add_feat(self, feat):
        self.feats.append(vars(feat))
    def del_feat(self, feat):
        self.feats.remove(feat)
    def add_equipment(self, item):
        self.equipment.append(item)
    def del_equipment(self, item):
        self.equipment.remove(item)
    def add_weapon(self, weapon):
        self.weapons.append(vars(weapon))
    def del_weapon(self, weapon):
        self.weapons.remove(weapon)
    def add_pool(self, pool):
        self.pools.append(pool)
    def del_pool(self, pool):
        self.pools.remove(pool)
    def add_spell(self, spell):
        self.spells.append(vars(spell))
    def del_spell(self, spell):
        self.spells.remove(spell)
    def add_spell_slot(self, level: int):
        try:
            self.spell_slots[level] += 1
            self.current_spell_slots[level] = self.spell_slots[level]
        except:
            self.spell_slots.add(level, 1)
            self.current_spell_slots[level] = self.spell_slots[level]
    def set_spell_slot(self, level: int, slots: int):
        try:
            self.spell_slots[level] = slots
            self.current_spell_slots[level] = self.spell_slots[level]
        except:
            self.spell_slots[level] = slots
            self.current_spell_slots[level] = self.spell_slots[level]
    def use_spell_slot(self, level):
        level = int(level)
        if self.current_spell_slots[level] > 0:
            self.current_spell_slots[level] += -1
        else:
            self.current_spell_slots[level] = 0
            print('Zero slots available!')
    def replenish_spell_slots(self):
        self.current_spell_slots = self.spell_slots
    def set_hitDice(self, dice):
        self.hitDice = dice
    def set_current_hit_dice(self, dice):
        self.currentHitDice = dice
    def set_hit_die(self, die):
        self.hit_die = die
    def add_prof(self, prof):
        self.proficiencies.append(prof)
    def set_initiative_bonus(self, bonus):
        self.initiative_bonus = bonus
    
    def damage(self, damage):
        self.hpCurrent = int(self.hpCurrent) - int(damage)
        if int(self.hpCurrent) <= 0:
            self.hpCurrent = 0
            self.isDown = True
    def heal(self, heal):
        self.hpCurrent = int(self.hpCurrent) + int(heal)
        if self.isDown == True:
            self.isDown = False
        if int(self.hpCurrent) > int(self.hpMax):
            self.hpcurrent = int(self.hpMax)
    def extra_hp(self, extra):
        self.extra_hp = extra
    def raise_char(self):
        self.isDown = False
        
    def save_character(self, filename):
        config = configparser.ConfigParser()
        config['STATS'] = {'name':self.name,
                           'race':self.race,
                           'subrace':self.subrace,
                           'languages':self.languages,
                           'charClass':self.charClass,
                           'level':self.level,
                           'proficiency':self.prof,
                           'armorClass':self.armorClass,
                           'strength':self.strength,
                           'dex':self.dex,
                           'constitution':self.con,
                           'intelligence':self.intelligence,
                           'wisdom':self.wisdom,
                           'charisma':self.charisma,
                           'hpMax':self.hpMax,
                           'hitDice':self.hitDice,
                           'hit_die':self.hit_die,
                           'proficiencies':self.proficiencies,
                           'initiative_bonus':self.initiative_bonus,
                           'actions':self.actions,
                           'feats':self.feats,
                           'spells':self.spells,
                           'spell_slots':self.spell_slots}
        pool_list = []
        for pool in self.pools:
            pool_list.append(vars(pool))
        config['STATUS'] = {'hpCurrent':self.hpCurrent,
                           'isDown':self.isDown,
                           'inspiration':self.inspiration,
                           'currentHitDice':self.currentHitDice,
                           'pools':pool_list,
                           'current_spell_slots':self.current_spell_slots}
        config['EQUIPMENT'] = {'gold':self.gold,
                               'equipment':self.equipment,
                               'weapons':self.weapons}  
                               
        with open(filename, 'w') as configfile:
            config.write(configfile)
    class Action:
        
        def __init__(self, name: str, description = ''):
            self.name = name
            self.description = description
    
    class Feat:
    
        def __init__(self, name: str, description = ''):
            self.name = name
            self.description = description
    
    class Weapon:
    
        def __init__(self, name: str, dmg = '', description = ''):
            self.name = name
            self.dmg = dmg
            self.description = description
            
    class Pool:
        def __init__(self, name: str, max: int, current = 0):
            self.name = name
            self.max = max
            self.current = current
        def use(self, amount):
            self.current = int(self.current) - int(amount)
            if int(self.current) < 0:
                self.current = 0
        def replenish(self, amount):
            self.current = int(self.current) + int(amount)
            if int(self.current) > int(self.max):
                self.current = self.max
        def get_current(self):
            return self.current
        def increase_max(self, new_max):
            self.max = new_max
        def change_name(self, name):
            self.name = name
    
    class Spell:
        def __init__(self, name: str, level: int, description = """"""):
            self.name = name
            self.level = level
            self.description = description
                
def load_character(file):
    config = configparser.ConfigParser()
    #filename = str(path) + '/characters/' + file + '.ini'
    config.read(file)
    ch = Character(config['STATS']['level'],config['STATS']['proficiency'],config['STATS']['armorClass'],config['STATS']['strength'],config['STATS']['dex'],config['STATS']['constitution'],config['STATS']['intelligence'],config['STATS']['wisdom'],config['STATS']['charisma'],config['STATS']['hpMax'],config['EQUIPMENT']['gold'],name = config['STATS']['name'],race = config['STATS']['race'],subrace = config['STATS']['subrace'],charClass = config['STATS']['charClass'], hitDice = config['STATS']['hitdice'])
    ch.initiative_bonus = config['STATS']['initiative_bonus']
    ch.inspiration = config['STATUS']['inspiration']
    ch.hpCurrent = config['STATUS']['hpCurrent']
    ch.currentHitDice = config['STATUS']['currentHitDice']
    ch.isDown = eval(config['STATUS']['isDown'])
    try:
        ch.languages = eval(config['STATS']['languages'])
    except:
        pass
    try:
        for pool in eval(config['STATUS']['pools']):
            name = pool['name']
            max = pool['max']
            current = pool['current']
            new_pool = ch.Pool(name, max, current = current)
            ch.add_pool(new_pool)
    except:
        pass
    try:
        ch.actions = eval(config['STATS']['actions'])
    except:
        pass
    try:
        ch.feats = eval(config['STATS']['feats'])
    except:
        pass
    try:
        ch.spells = eval(config['STATS']['spells'])
    except:
        pass
    try:
        ch.spell_slots = eval(config['STATS']['spell_slots'])
    except:
        pass
    try:
        ch.current_spell_slots = eval(config['STATUS']['current_spell_slots'])
    except:
        pass
    try:
        ch.hit_die = config['STATS']['hit_die']
    except:
        logging.debug('hit_die not loaded!')
        pass
    proficiencies = eval(config['STATS']['proficiencies'])
    ch.proficiencies = [string.casefold() for string in proficiencies]
    ch.equipment = eval(config['EQUIPMENT']['equipment'])
    ch.weapons = eval(config['EQUIPMENT']['weapons'])
    return ch
    #try:
    #    config.read(file)
    #    ch = Character(config['STATS']['level'],config['STATS']['profenciency'],config['STATS']['armorClass'],config['STATS']['strength'],config['STATS']['dex'],config['STATS']['constitution'],config['STATS']['intelligence'],config['STATS']['wisdom'],config['STATS']['charisma'],config['STATS']['hpMax'],config['EQUIPMENT']['gold'],name = config['STATS']['name'],race = config['STATS']['race'],subrace = config['STATS']['subrace'],languages = config['STATS']['languages'],charClass = config['STATS']['charClass'],weapons = config['EQUIPMENT']['weapons'])
    #    ch.insp = config['STATUS']['inspiration']
    #    ch.hpCurrent = config['STATUS']['hpCurrent']
    #    ch.isDown = config['STATUS']['isDown']
    #    for e in config['Equipment']['equipment']:
    #        ch.add_equipment(e)
    #    return ch
    #except:
    #    print('Save file not found!')
    #    return null