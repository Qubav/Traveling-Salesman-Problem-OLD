from matplotlib import pyplot as plt
import time
from TSP import get_coordinates, get_optimal_order, get_distance_table, FI_algorithm, Tabu_Search, get_tour_distance, TS_daily_tours


if(__name__ == "__main__"):

    print("Możliwe wybory zestawu danych:\n1 - Berlin52\n2 - Att48\n3 - Eil101\n")
    data_set_number = int(input("Wprowadź liczbę 1, 2 bądź 3 aby wybrać zestaw danych.\n"))
    while(data_set_number != 1 and data_set_number != 2 and data_set_number != 3):
        data_set_number = int(input("Wprowadź liczbę 1, 2 bądź 3 aby dokonać wyboru zestawu danych!\n"))

    if(data_set_number == 1):
        # otwarcie, odczytanie i wypisanie optymalnej kolejności
        with open("berlin52.opt.tour.txt", "r") as f:
            order_opt_list = f.read().splitlines()

        # otwarcie i wczytanie pliku
        with open("berlin52.txt", "r") as f:
            city_list = f.read().splitlines()

    elif(data_set_number == 2):
        with open("att48.opt.txt", "r") as f:
            order_opt_list = f.read().splitlines()

        with open("att48.txt", "r") as f:
            city_list = f.read().splitlines()

    elif(data_set_number == 3):

        with open("eil101.opt.txt", "r") as f:
            order_opt_list = f.read().splitlines()

        with open("eil101.txt", "r") as f:
            city_list = f.read().splitlines()

    order_opt = get_optimal_order(order_opt_list)
    x, y = get_coordinates(city_list, 6)
    dist_mat = get_distance_table(x, y)

    # building algorithm
    start_time_FI = time.time()
    order = FI_algorithm(x, y, dist_mat)
    exec_time_FI = time.time() - start_time_FI
    print("FI exec time:", exec_time_FI)

    print("Wybierz:\n1 jeśli chcesz aby dniówki były uwzględnione\n2 jeśli chcesz aby nie były uwzględniane")
    dniowki_number = int(input("Wprowadź liczbę 1 bądź 2.\n"))
    while(data_set_number != 1 and data_set_number != 2):
        dniowki_number = int(input("Wprowadź liczbę 1 bądź 2!\n"))

    if(dniowki_number == 1):
        dniowki = True
    else:
        dniowki = False
    
    tabu_tenure = 12
    iterations = 250

    f = []
    d = []
    start_time = time.time()
    best_solution = Tabu_Search(order, tabu_tenure, dist_mat, iterations, f, d)
    exec_time = time.time() - start_time

    print("czas dzialania TS", exec_time)
    td = get_tour_distance(order, dist_mat)
    print("Algorytm budujacy FI", td)
    td_opt = get_tour_distance(order_opt, dist_mat)
    print("Optymalna kolejnosc", td_opt)
    g = (td - td_opt) / td_opt * 100
    print("Roznica w długości trasy algorytmu budujacego i optymalnej kolejnosco", g, "%.")
    td_ts = get_tour_distance(best_solution, dist_mat)
    print("FI + TS", td_ts)
    g_ts = (td_ts - td_opt) / td_opt * 100
    print("Roznica w długości trasy algorytmu budujacego i optymaluzujacego TS i optymalnej kolejnosco", g_ts, "%.")

    if(dniowki is True):
        ff = []
        dd = []
        gg = []
        fff = []
        ddd = []
        ggg = []
        limit = 12000
        iterations = 50
        base = 13
        tabu_tenure = 10
        start_daily = time.time()
        daily_best, best_daily_tour_count = TS_daily_tours(order, limit, base, tabu_tenure, dist_mat, iterations, ff, dd, gg, fff, ddd, ggg)
        end_daily = time.time() - start_daily
        print("czas dzialania TS dniowki", end_daily)
        print(daily_best)

    
    if(dniowki is True):
        td_db = get_tour_distance(daily_best, dist_mat)
        print("Dionwki dystans laczny", td_db)
        g_ts = (td_db - td_opt) / td_opt * 100
        print("Roznica w długości trasy dniówek TS i optymalnej kolejnosco", g_ts, "%.")



     # rysowanie koordynatów na mapie
    plt.figure(1)
    plt.title("Trasa dla algorytmu kontrukcyjnego FI")
    x2 = []
    y2 = []

    for i in range(0, len(order), 1):
        x2.append(x[order[i]])
        y2.append(y[order[i]])

    plt.ylabel("współrzędne y")
    plt.xlabel("współrzędne x")


    plt.plot(x2, y2, "o-k", linewidth = 1.5, markersize = 3.0)

    plt.figure(2)
    plt.title("Trasa przebiegająca według optymalnej kolejności")
    x3 = []
    y3 = []

    for i in range(0, len(order_opt), 1):
        x3.append(x[order_opt[i]])
        y3.append(y[order_opt[i]])

    plt.ylabel("współrzędne y")
    plt.xlabel("współrzędne x")


    plt.plot(x3, y3, "o-k", linewidth = 1.5, markersize = 3.0)

    plt.figure(3)
    plt.title("Trasa przebiegająca według kolejności wyznaczonej Tabu Search")
    x4 = []
    y4 = []

    for i in range(0, len(best_solution), 1):
        x4.append(x[best_solution[i]])
        y4.append(y[best_solution[i]])
    
    plt.ylabel("współrzędne y")
    plt.xlabel("współrzędne x")


    plt.plot(x4, y4, "o-k", linewidth = 1.5, markersize = 3.0)

    if(dniowki is True):
        plt.figure(5)
        plt.title("Wykres przedstawiający przebieg wyznaczonych tras\n dla kolejnych dniówek")
        colors = ["royalblue", "limegreen", "darkorange", "magenta", "midnightblue", "firebrick", "deeppink", "grey", "deepskyblue", "sienna", "lime", "gold", "turquoise", "darkcyan", "purple", "darkgoldenrod", "brown", "darkolivegreen", "orange"]
        numeracja = ['pierwsza dniówka', 'druga dniówka', 'trzecia dniówka', 'czwarta dniówka', 'piąta dniówka', 'szósta dniówka', 'siódma dniówka', 'ósma dniówka', 'dziewiąta dniówka', 'dziesiąta dniówka', 'jedenasta dniówka', 'dwunasta dniówka', 'trzynasta dniówka', 'czternasta dniówka', 'piętansta dniówka', 'szesnasta dniówka', 'siedemnasta dniówka', 'osiemnasta dniówka', 'dziewiętnasta dniówka', 'dwudziesta dniówka']
        
        x5 = []
        y5 = []
        base = daily_best[0]
        bases = []

        for i in range(0, len(daily_best), 1):
            x5.append(x[daily_best[i]])
            y5.append(y[daily_best[i]])
            if(daily_best[i] == base):
                bases.append(i)

        for i in range(0, best_daily_tour_count):
            plt.plot(x5[bases[i]:(bases[i + 1] + 1)], y5[bases[i]:(bases[i + 1] + 1)], "-o", color = colors[i], label = numeracja[i], linewidth = 1.5, markersize = 3.0)

        
        plt.plot(x5[0], y5[0], "-o", color = "black", markersize = 9, label = "Baza" )
        plt.legend()

        plt.figure(6)
        plt.figure(6).set_figheight(7)
        plt.figure(6).set_figwidth(7)
        plt.suptitle("Wykresy łącznej ilości godzin potrzebnej na pokonanie wyznaczonej trasy\noraz łącznej długości trasy")
        x6 = []
        y6 = []
        z6 = []
        xx6 = []
        yy6 = []
        zz6 = []

        for i in range(0, len(ff)):
            x6.append((ff[i] - 1 + (dd[i] / limit)))
            y6.append((ff[i] + dd[i] / limit - 1) * 8)
            z6.append(gg[i])
            xx6.append((fff[i] - 1 + (ddd[i] / limit)))
            yy6.append((fff[i] + ddd[i] / limit - 1) * 8)
            zz6.append(ggg[i])
        
        plt.subplot(2, 1, 1)
        plt.title("Liczba godzin potrzebnych na pokonanie wyznaczonych tras")
        plt.plot(y6, color = "royalblue", label = "wartość dla najlepszego sąsiada w danej iteracji")
        plt.plot(yy6, color = "darkorange", label = "wartość dla najlepszego rozwiązania")
        plt.legend()
        plt.xlabel("iteracje")
        plt.ylabel("liczba godzin")
        plt.subplot(2, 1, 2)
        plt.title("Suma długości wyznaczonych tras")
        plt.plot(z6,  color = "royalblue", label = "wartość dla najlepszego sąsiada w danej iteracji")
        plt.plot(zz6, color = "darkorange", label = "wartość dla najlepszego rozwiązania")
        plt.xlabel("iteracje")
        plt.ylabel("długość trasy")
        plt.legend()


    plt.figure(7)
    plt.plot(f, label = "długość trasy wyznaczonej w danej iteracji", color = "royalblue")
    plt.plot(d, label = "długość najkorzystniejszej trasy\n wyznaczona do danej iteracji", color = "darkorange")
    plt.legend()
    plt.title("Wykres długości trasy na przestrzeni kolejnych iteracji")
    plt.xlabel("iteracje")
    plt.ylabel("długość trasy")
    plt.show()