import os
import subprocess
import random
import matplotlib.pyplot as plt
import numpy as np

# Setari
SOURCE = "src/main.c"
EXE = "knapsack_solver"
TEST_DIR = "tests"

def compile_code():
    print("Compilez codul...")
    try:
        subprocess.check_call(["gcc", "-O3", SOURCE, "-o", EXE])
        print("Compilare OK.")
    except:
        print("Eroare la compilare!")
        exit(1)

def generate_test(path, n, cap, correlated=False):
    with open(path, "w") as f:
        f.write(f"{n} {cap}\n")
        for _ in range(n):
            w = random.randint(1, 100)
            if correlated:
                v = w + 10
            else:
                v = random.randint(1, 100)
            f.write(f"{w} {v}\n")

def run_test(algo, path):
    # algo: 0=DP, 1=Greedy, 2=Backtracking
    with open(path, "r") as f:
        p = subprocess.Popen([f"./{EXE}", str(algo)], stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = p.communicate()
        
        if p.returncode != 0:
            raise Exception("Eroare runtime")
            
        res = out.strip().split()
        return int(res[0]), float(res[1])

def main():
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR)
    
    compile_code()

    # EXPERIMENT 0: BACKTRACKING vs RESTUL
    print("\nExperiment 0: Backtracking vs DP vs Greedy")
    
    ns_small = [2, 4, 8, 16, 32] 
    W_fixed = 500
    
    t_back = []
    t_dp_sm = []
    t_gr_sm = []
    
    for n in ns_small:
        fname = f"{TEST_DIR}/small_{n}.in"
        generate_test(fname, n, W_fixed, False)
        
        # Rulam toti 3 algoritmii
        _, time_bt = run_test(2, fname) # Backtracking
        _, time_dp = run_test(0, fname) # DP
        _, time_gr = run_test(1, fname) # Greedy
        
        t_back.append(time_bt)
        t_dp_sm.append(time_dp)
        t_gr_sm.append(time_gr)
        
        print(f"N = {n}: Backtracking = {time_bt:.4f}s , DP = {time_dp:.5f}s , Greedy = {time_gr:.5f}s")

    # Grafic Special pentru Backtracking
    plt.figure(figsize=(10, 6))
    plt.plot(ns_small, t_back, label='Backtracking (Exponential)', marker='o', color='red')
    plt.plot(ns_small, t_dp_sm, label='DP (Polinomial)', marker='s', color='blue')
    plt.plot(ns_small, t_gr_sm, label='Greedy (Liniar)', marker='^', color='green')
    plt.xlabel('Numar Obiecte (N)')
    plt.ylabel('Timp (s)')
    plt.title('Backtracking vs Greedy vs Programare Dinamica')
    plt.legend()
    plt.grid(True)
    plt.savefig("grafic_backtracking.png")
    print("Grafic salvat: grafic_backtracking.png")


    # EXPERIMENT 1: SCALABILITATE (Doar DP si Greedy), Backtracking ar dura prea mult pentru N mare
    print("\nExperiment 1: Timp executie")
    
    ns = [50, 100, 500, 1000, 2000, 5000, 10000, 100000]
    t_dp = []
    t_greedy = []
    
    for n in ns:
        fname = f"{TEST_DIR}/time_{n}.in"
        generate_test(fname, n, 2000, False)
        
        _, time_dp = run_test(0, fname)
        _, time_gr = run_test(1, fname)
        
        t_dp.append(time_dp)
        t_greedy.append(time_gr)
        print(f"N = {n}: DP = {time_dp:.5f}s, Greedy = {time_gr:.5f}s")

    plt.figure(figsize=(10, 6))
    plt.plot(ns, t_dp, label='DP', marker='o')
    plt.plot(ns, t_greedy, label='Greedy', marker='x')
    plt.xlabel('Numar Obiecte (N)')
    plt.ylabel('Timp (s)')
    plt.title('Comparatie Timp: DP vs Greedy (pe seturi de date cu N mare)')
    plt.legend()
    plt.grid(True)
    plt.savefig("grafic_timp.png")
    print("Grafic salvat: grafic_timp.png")


    # EXPERIMENT 2: ACURATETE
    print("\nExperiment 2: Acuratete Greedy")
    ns_acc = [10, 50, 100, 200, 500]
    acc_list = []
    
    for n in ns_acc:
        fname = f"{TEST_DIR}/acc_{n}.in"
        generate_test(fname, n, n*10, True)
        
        val_dp, _ = run_test(0, fname)
        val_gr, _ = run_test(1, fname)
        
        if val_dp == 0: val_dp = 1
        procent = (val_gr / val_dp) * 100
        acc_list.append(procent)
        print(f"N = {n}: DP = {val_dp}, Greedy = {val_gr} -> {procent:.2f}%")

    plt.figure(figsize=(8, 5))
    plt.bar([str(x) for x in ns_acc], acc_list, color='orange')
    plt.title('Acuratete Greedy')
    plt.ylim(80, 100)
    plt.savefig("grafic_acuratete.png")
    print("Grafic salvat: grafic_acuratete.png")


    # EXPERIMENT 3: MEMORIE
    print("\nExperiment 3: Memorie (W = 10 miliarde)")
    
    big_W = 10000000000
    fname = f"{TEST_DIR}/stress.in"
    generate_test(fname, 10, big_W, False)
    
    print(f"Se incepe rularea cu W = {big_W}...")

    print("Programare Dinamica: ", end="")
    try:
        run_test(0, fname)
        print("Rularea a functionat -> Suficienta memorie libera!")
    except:
        print("A crapat -> Insuficienta memorie libera!")

    print("Greedy: ", end="")
    try:
        val, t = run_test(1, fname)
        print(f"Succes! Rezultat = {val}, Timp = {t:.5f}s")
    except Exception as e:
        print(f"Eroare: {e}")

if __name__ == "__main__":
    main()
