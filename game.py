import random
from player import Player
import asyncio


class Game():
    players=[]
    temp=True
    stan=True
    app=""
    umarli=[]
    mi=0
    syn=0
    ma=0
    zabijanie_licznik=0
    pojedynki_licznik=0
    async def cout(*names):
        if len(names)==1:
            for name in names:
                await Game.app.out(name)
        else:
            for name in names:
                await Game.app.out(name+" ")

    
    async def wczyt(name=None):
        return await Game.app.in_str(name)
    
    async def wczyt_int(name=None):
        n=await Game.app.in_t(name)
        await Game.app.out(str(n)+"\n")
        return n

    async def start():
        state="day"
        await Game.generate_players(Game.mi,Game.syn,Game.ma)
        await Game.generate_fractions()

    async def do_day():
        if len(Game.players)==1:
            Game.stan=False
        else:
            await Game.cout("DZIEŃ \n")
            await Game.list_dead_night()
            await Game.list_players()
            Game.temp=True
            while Game.temp:
                n = await Game.wczyt()
                await Game.helper_day(n)
        
    async def do_night():
        if Game.stan==True:
            await Game.cout("NOC\n")
            await Game.list_players()
            await Game.lekarz_leczenie()
            await Game.pawulon_pawulonienie()
            await Game.katani_katanienie()
            await Game.mafia_killing()
            await Game.angel_killing()


        else:
            pass

    async def lekarz_leczenie():
        if Game.is_alive("lekarz"):
            n= await Game.wczyt_int("podaj numer osoby do wyleczenia\n")
            Game.players[n-1].add_temp("leczenie")
        else:
            await Game.cout("lekarz nie żyje, improwizuj!\n")

    async def pawulon_pawulonienie():
        if Game.is_alive("pawulon"):
            n=await Game.wczyt_int("podaj numer osoby do zapawulonienia\n")
            Game.players[n-1].add_temp("pawulon")
        else:
            await Game.cout("pawulon nie żyje, improwizuj!\n")
    
    async def mafia_killing():
        temp=False
        for p in Game.players:
            if p.frac==-1:
                temp=True
        if temp:
            n=await Game.wczyt_int("Podej numer osoby do zabicia\n")
            if Game.players[n-1].kill_mafia():
                Game.umarli.append(n)
            else:
                await Game.cout("lekarz zadziałał\n")
    
    async def angel_killing():
        if Game.is_alive("anioł"):
            n=await Game.wczyt("podaj numer osoby do naznaczenia\n")
            if Game.players[n-1].add_angel_counter():
                Game.umarli.append(n)
        else:
            await Game.cout("anioł nie żyje, improwizuj!\n")


    async def glosowanko():
        await Game.cout("podaj graczy\n")
        index_1=await Game.wczyt_int()
        index_2=await Game.wczyt_int()
        await Game.cout("podaj rozkład głosów\n")
        gl_1=await Game.wczyt_int()
        gl_2=await Game.wczyt_int()
        return [index_1,index_2,gl_1,gl_2]

    async def helper_day(n):
        if n=="noc":
            Game.temp=False
        elif n=="pojedynek":
            await Game.pojedynek()
        elif n=="sprawdzanie":
            await Game.sprawdzanie()
        elif n=="zabijanie":
            await Game.zabijanie()
        elif n=="świr":
            pass
        elif n=="staty":
            await Game.staty()
        elif n=="gracze":
            await Game.list_players()
        elif n=="help":
            await Game.help()
        elif n=="clean":
            await Game.app.reset_label()
        elif n=="kill":
            await Game.admin_kill()
        else:
            await Game.cout("komenda nieznana\n")

    async def katani_katanienie():
        if Game.is_alive("katani"):
            n=await Game.wczyt("podaj numer osoby do katanienia\n")
            await Game.cout("ta osoba jest taka {}\n".format(Game.players[n-1].check_status()))
        else:
            await Game.cout("katanie nie żyje, improwizuj!\n")

    async def zabijanie():
        if Game.zabijanie_licznik==0:
            i1,i2,g1,g2=await Game.glosowanko()
            if g1>g2:
                Game.players[i2-1].kill()
                await Game.cout("umiera gracz nr {}\n".format(i2))
                del Game.players[i2-1]
            else:
                Game.players[i1-1].kill()
                del Game.players[i1-1]
                await Game.cout("umiera gracz nr {}\n".format(i1))
            Game.zabijanie_licznik+=1
        else:
            await Game.cout("głosowanie już się odbyło\n")
    
    async def pojedynek():
        if Game.pojedynki_licznik<3:
            i1,i2,g1,g2=await Game.glosowanko()
            if g1==g2:
                if g1==0:
                    await Game.cout("zerowy remis, nikt nie umiera\n")
                else:
                    await Game.cout("niezerowy remis\n")
                    Game.players[i1-1].kill()
                    Game.players[i2-1].kill()
                    del Game.players[i2-1]
                    del Game.players[i1-1]
            elif g1>g2:
                Game.players[i2-1].kill()
                del Game.players[i2-1]
                await Game.cout("umiera gracz nr {}\n".format(i2))
            else:
                Game.players[i1-1].kill()
                del Game.players[i1-1]
                await Game.cout("umiera gracz nr {}\n".format(i1))

            Game.pojedynki_licznik+=1
        else:
            await Game.cout("Limit pojedynków osiągnięty\n")
    async def sprawdzanie():
        if Game.zabijanie_licznik==0:
            i1,i2,g1,g2=await Game.glosowanko()
            if g1>g2:
                Game.cout(Game.players[i2-1].check())
            else:
                Game.cout(Game.players[i1-1].check())
            Game.zabijanie_licznik+=1
        else:
            await Game.cout("głosowanie już się odbyło\n")

    async def swirowanie(index):
        Game.players[index-1].kill()
        del Game.players[index-1]

    async def generate_players(mi,s,ma):
        i=1
        for _ in range(0,mi):
            Game.players.append(Player("player"+str(i),1))
            i+=1

        for _ in range(0,s):
            Game.players.append(Player("player"+str(i),0))
            i+=1

        for _ in range(0,ma):
            Game.players.append(Player("player"+str(i),-1))
            i+=1
        random.shuffle(Game.players)

    async def generate_fractions():
        pass

    async def list_dead_night():
        for n in Game.umarli:
            await Game.cout("umarł gracz nr {}\n".format(n))
        Game.umarli=[]
        a=0
        b=0
        c=0
        for pl in Game.players:
            if pl.frac==1:
                a+=1
            elif pl.frac==0:
                b+=1
            else:
                c+=1
        Game.mi=a
        Game.syn=b
        Game.ma=c
        await Game.staty()
        Game.zabijanie_licznik=0
        Game.pojedynki_licznik=0

    async def list_players():
        for p in Game.players:
            if p.alive:
                await Game.cout(p.name,Game.con(p.frac),p.function)
        await Game.cout("\n")

    async def admin_kill():
        n=await Game.wczyt_int("podaj gracza do zabicia\n")
        Game.players[n-1].kill_admin()
        del Game.players[n-1]

    def is_alive(func):
        for player in Game.players:
            if player.function==func:
                return True
        return False
    
    def con(i):
        if i==1:
            return "miasto"
        elif i==0:
            return "syndyk"
        else:
            return "mafia"

    async def gen_num():
        Game.mi=await Game.wczyt_int("Podaj liczbę miasta\n")
        Game.syn=await Game.wczyt_int("Podaj liczbę syndykatu\n")
        Game.ma=await Game.wczyt_int("Podaj liczbę mafii\n")

    async def run(mi,s,ma):
        await Game.gen_num()
        await Game.start()
        while Game.stan:
            await Game.do_day()
            await Game.do_night()
        await Game.cout("koniec gry\n")


    async def help():
        await Game.cout("Dostępne komendy\n")
        await Game.cout("sprawdzanie\n")
        await Game.cout("zabijanie\n")
        await Game.cout("swir\n")
        await Game.cout("pojedynek\n")
        await Game.cout("gracz-lista graczy\n")
        await Game.cout("noc\n")

    async def staty():
        await Game.cout("statystyki to {}-{}-{}\n".format(Game.mi,Game.syn,Game.ma))
