class weapon:
    def __init__(self, damage, hs_damage, cc, cd, fr, ms, rt):
        self.damage = damage
        self.hs_damage = hs_damage
        self.cc = cc
        self.cr = 50*self.cc/(75-self.cc)
        self.cp = (75*self.cr)/(self.cr+50)
        self.cd = cd
        self.fr = fr
        self.ms = ms
        self.rt = rt
        self.max_damage = self.damage*(1+self.cd/100)
        self.max_hs_damage = self.hs_damage*(1+self.cd/100)
        self.med_damage = self.damage + \
            (self.damage*1+(self.cp/100))*(1+self.cd/100)
        self.med_hs_damage = self.hs_damage + \
            (self.hs_damage*(1+(self.cp/100)*(1+self.cd/100)))
        self.dps = (self.med_damage*self.ms)/((self.ms-1)*(1/self.fr)+self.rt)
        self.hs_dps = (self.med_hs_damage*self.ms) / \
            ((self.ms-1)*(1/self.fr)+self.rt)

    def optimise_dps(self, md=30, mcp=30, mcd=135, mfr=42, mrt=75):

        damage_mod, cp_mod, cd_mod, fr_mod, rt_mod = ((1+md/100)*self.damage), ((75*(self.cr+mcp))/(
            self.cr+mcp+50)), (self.cd+mcd), (self.fr*(1+mfr/100)), (self.rt/(1+mrt/100))
        print("self.damage ", self.damage, " damage_mod ", damage_mod)
        print("self.cp ", self.cp, " cp_mod ", cp_mod)
        print("self.cd ", self.cd, " cd_mod ", cd_mod)
        print("self.fr ", self.fr, " fr_mod ", fr_mod)
        print("self.rt ", self.rt, " rt_mod ", rt_mod)
        print("self.dps", self.dps)

        dps_perk_damage = (((damage_mod)+((damage_mod)*(1+self.cp/100)
                           * (1+self.cd/100))*self.ms)/((self.ms-1)*(1/self.fr)+self.rt))
        dps_perk_cc = (((self.damage)+((self.damage)*((1+cp_mod/100)
                       * (1+self.cd/100))*self.ms)/((self.ms-1)*(1/self.fr)+self.rt)))
        dps_perk_cd = (((self.damage)+((self.damage)*(1+self.cp/100)
                       * (1+(cd_mod)/100))*self.ms)/((self.ms-1)*(1/self.fr)+self.rt))
        dps_perk_fr = (((self.damage)+((self.damage)*(1+self.cp/100)
                       * (1+(self.cd)/100))*self.ms)/((self.ms-1)*(1/fr_mod)+self.rt))
        dps_perk_rt = (((self.damage)+((self.damage)*(1+self.cp/100)
                       * (1+(self.cd)/100))*self.ms)/((self.ms-1)*(1/self.fr)+rt_mod))
        list_perk = [["perk_damage", dps_perk_damage], ["perk_cc", dps_perk_cc], [
            "perk_cd", dps_perk_cd], ["perk_fr", dps_perk_fr], ["perk_fr", dps_perk_rt]]
        return list_perk

    # def test(self):
    # matrix1 = [[30,0,0,0,0],[0,30,0,0,0],[0,0,135,0,0],[0,0,0,42,0],[0,0,0,0,75]]
    # for i in matrix1:
    # a = (((self.damage*(1+i[0]/100))+((self.damage*(1+i[0]/100))*(1+(75*(self.cr+i[1]))/((self.cr+i[1]+50)/100))*(1+(self.cd+i[2])/100)))*self.ms)/((self.ms-1)*(1/self.fr*(1+i[3]/100))+self.rt*(1+i[4]/100))
    # print("self.damage*(1+{i[0]}")

    def optimise_max_hs_damage(self):

        # Stocker les choix d'avantages comme étant des matrices de modificateurs
        matrix1 = [[30, 0, 0, 0, 0], [0, 30, 0, 0, 0], [0, 0, 135, 0, 0], [0, 0, 0, 42, 0], [
            0, 0, 0, 0, 75]]  # matrice perk 1 : 0 = damage, 1 = cr, 2 = cd, 3 = fr, 4 = rt
        # matrice perk 2 : 0 = ms , 1 = rt
        matrix2 = [[75, 0], [0, 75]]
        # matrice perk 3 : 0 = physique, 1 = énergie
        matrix3 = [[44, 0], [0, 20]]
        matrix4 = [[0, 0, 0, 0, 0], [0, 30, 0, 0, 0], [0, 0, 135, 0, 0], [0, 0, 0, 30, 0], [
            0, 0, 0, 0, 75]]  # matrice perk 4 : 0 = headshot, 1 = cr, 2 = cd, 3 = damage, 4 = ms
        # matroce perk 5 : 0 = affixe, 1 = boss
        matrix5 = [[45, 0], [0, 36]]
        out = {}
        for i in matrix1:
            for j in matrix2:
                for k in matrix3:
                    for l in matrix4:
                        for m in matrix5:
                            damage_mod, cp_mod, cd_mod, fr_mod, rt_mod, ms_mod = ((1+(i[0]+k[0]+k[1]+l[3]+m[0]+m[1])/100)*self.damage), ((75*(self.cr+i[1]+l[1]))/(
                                self.cr+i[1]+l[1]+50)), (self.cd+i[2]+l[2]), (self.fr*(1+i[3]/100)), (self.rt/(1+(i[4]+j[1])/100)), (self.ms*(1+(j[0]+l[4])/100))
                            a = ((damage_mod+(damage_mod*(1+cp_mod/100)*(1+cd_mod/100)))
                                 * ms_mod)/((ms_mod-1)*(1/fr_mod)+rt_mod)
                            b = "((1+({0}+{1}+{2}+{3}+{4}+{5})/100)*self.damage)+(((1+({0}+{1}+{2}+{3}+{4}+{5})/100)*self.damage)*(1+((75*(self.cr+{6}+{7}))/(self.cr+{6}+{7}+50)))*(self.cd+{13}+{14}))*(self.ms*(1+({8}+{9})/100))/((self.ms*(1+({8}+{9})/100))*(1/(self.fr*(1+{10}/100)))+(self.rt/(1+({11}+{12})/100))))".format(
                                i[0], k[0], k[1], l[3], m[0], m[1], i[1], l[1], j[0], l[4], i[3], i[4], j[1], i[2], l[2])
                            out.update({a: b})
                            # print(b)
                            # print("Résultat : ",a)
        print(max(out.keys()))
        print(out[max(out.keys())])

    def test(self):

        dico1 = [[30, "Damage", 0, "", 0, "", 0, "", 0, ""], [0, "", 30, "Crit Rating", 0, "", 0, "", 0, ""], [00, "", 0, "", 135, "Crit Damage", 0, "", 0, ""], [
            00, "", 0, "", 0, "", 42, "Fire Rate", 0, ""], [0, "", 0, "", 0, "", 0, "", 75, "Reload Time"]]  # matrice perk 1 , 0 = damage, 1 = cr, 2 = cd, 3 = fr, 4 = rt
        dico2 = [[75, "Magazine Size", 0, "Reload Time"], [0, "Magazine Size",
                                                           75, "Reload Time"]]														# matrice perk 2 , 0 = ms , 1 = rt
        # matrice perk 3 , 0 = physique, 1 = énergie
        dico3 = [[44, "Physic", 0, "Element"], [0, "Physic", 22, "element"]]
        dico4 = [[0, "Headshot Damage", 0, "Crit Rating", 0, "Crit Damage", 0, "Fire Rate", 0, "Reload Time"], [0, "Headshot Damage", 30, "Crit Rating", 0, "Crit Damage", 0, "Fire Rate", 0, "Reload Time"], [00, "Headshot Damage", 0, "Crit Rating", 135, "Crit Damage", 0, "Fire Rate",
                                                                                                                                                                                                               0, "Reload Time"], [00, "Headshot Damage", 0, "Crit Rating", 0, "Crit Damage", 42, "Fire Rate", 0, "Reload Time"], [0, "Damage", 0, "Crit Rating", 0, "Crit Damage", 0, "Fire Rate", 75, "Reload Time"]]  # matrice perk 4 , 0 = headshot, 1 = cr, 2 = cd, 3 = damage, 4 = ms
        dico5 = [[45, "affixe", 0, "Boss"], [0, "Affixe", 36, "Boss"]]

        out = []

        for i in dico1:
            for j in dico2:
                for k in dico3:
                    for l in dico4:
                        for m in dico5:
                            damage_mod, cp_mod, cd_mod, fr_mod, rt_mod, ms_mod = ((1+(i[0]+k[0]+k[2]+l[6]+m[0]+m[2])/100)*self.damage), ((75*(self.cr+i[2]+l[2]))/(
                                self.cr+i[2]+l[2]+50)), (self.cd+i[4]+l[4]), (self.fr*(1+i[6]/100)), (self.rt/(1+(i[8]+j[2])/100)), (self.ms*(1+(j[0]+l[8])/100))
                            a = ((damage_mod+(damage_mod*(1+cp_mod/100)*(1+cd_mod/100)))
                                 * ms_mod)/((ms_mod-1)*(1/fr_mod)+rt_mod)
                            b = "((1+({0}+{1}+{2}+{3}+{4}+{5})/100)*self.damage)+(((1+({0}+{1}+{2}+{3}+{4}+{5})/100)*self.damage)*(1+((75*(self.cr+{6}+{7}))/(self.cr+{6}+{7}+50)))*(self.cd+{13}+{14}))*(self.ms*(1+({8}+{9})/100))/((self.ms*(1+({8}+{9})/100))*(1/(self.fr*(1+{10}/100)))+(self.rt/(1+({11}+{12})/100))))".format(
                                i[1], k[1], k[3], l[7], m[1], m[3], i[3], l[3], j[1], l[9], i[7], i[9], j[3], i[5], l[5])
                            out += [b, a]

        print(out[:2])
        return out
        # print(max(out[:2+1]))
