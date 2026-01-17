#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct item {
    int id;
    int weight;
    int value;
} Item;

long long max_val_back = 0;

// GREEDY
// https://www.geeksforgeeks.org/fractional-knapsack-problem/

int compareRatio(const void *a, const void *b) {
    Item *itemA = (Item *)a;
    Item *itemB = (Item *)b;

    double r1 = (double)itemA->value / itemA->weight;
    double r2 = (double)itemB->value / itemB->weight;

    if (r1 < r2)
        return 1;
    if (r1 > r2)
        return -1;
    return 0;
}

long long solve_greedy(long long W, int n, Item *items) {
    qsort(items, n, sizeof(Item), compareRatio);

    long long current_value = 0;
    long long current_weight = 0;

    for (int i = 0; i < n; i++)
        if (current_weight + items[i].weight <= W) {
            current_weight += items[i].weight;
            current_value += items[i].value;
        }
    return current_value;
}

// PROGRAMARE DINAMICA
// https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/
// Vector unidimensional dp[W] pentru complexitate spatiala O(W)

long long solve_dp(long long W, int n, Item *items) {
    long long *dp = (long long *)calloc((W + 1), sizeof(long long));

    if (dp == NULL) {
        fprintf(stderr, "Eroare la alocarea memoriei in solve_dp!\n");
        exit(1);
    }

    for (int i = 0; i < n; i++) {
        // Parcurgem greutatile de la W la greutatea obiectului (invers)
        // Iteratorul w trebuie sa fie long long
        for (long long w = W; w >= items[i].weight; w--) {
            long long val_with_item = dp[w - items[i].weight] + items[i].value;
            if (val_with_item > dp[w])
                dp[w] = val_with_item;
        }
    }

    long long result = dp[W];
    free(dp);
    return result;
}

// BACKTRACKING
// https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/

void backtrack_recursive(int index, long long current_w, long long current_v, long long W, int n, Item *items) {
    if (current_w > W)
        return;

    if (current_v > max_val_back)
        max_val_back = current_v;

    if (index == n)
        return;

    if (current_w + items[index].weight <= W)
        backtrack_recursive(index + 1, current_w + items[index].weight, current_v + items[index].value, W, n, items);

    backtrack_recursive(index + 1, current_w, current_v, W, n, items);
}

long long solve_backtracking(long long W, int n, Item *items) {
    max_val_back = 0;
    backtrack_recursive(0, 0, 0, W, n, items);
    return max_val_back;
}

int main(int argc, char *argv[]) {
    if (argc < 2)
        return 1; 

    int algo = -1;
    if (strlen(argv[1]) != 1) {
        fprintf(stderr, "Eroare: Argument invalid.\n");
        return 1;
    }

    switch (argv[1][0]) {
        case '0':
            algo = 0;
            break;
        case '1':
            algo = 1;
            break;
        case '2':
            algo = 2;
            break;
        default:
            fprintf(stderr, "Eroare: Alege 0, 1 sau 2.\n");
            return 1;
    }

    int n;
    long long W;

    if (scanf("%d %lld", &n, &W) != 2)
        return 0;

    Item *items = (Item *)malloc(n * sizeof(Item));
    if (!items)
        return 1;

    for (int i = 0; i < n; i++) {
        items[i].id = i;
        if (scanf("%d %d", &items[i].weight, &items[i].value) != 2)
            break;
    }

    clock_t start = clock();
    long long result = 0;

    switch (algo) {
        case 0:
            result = solve_dp(W, n, items);
            break;
        case 1:
            result = solve_greedy(W, n, items);
            break;
        case 2:
            result = solve_backtracking(W, n, items);
            break;
    }

    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;

    printf("%lld %.6f\n", result, time_spent);

    free(items);
    return 0;
}
