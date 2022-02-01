from munkres import Munkres, DISALLOWED, print_matrix

m = Munkres()

A = [[0,1,2,2,5,3,DISALLOWED,DISALLOWED,DISALLOWED],
	 [2,1,2,2,3,DISALLOWED,5,DISALLOWED,DISALLOWED],
	 [2,1,0,0,3,DISALLOWED,DISALLOWED,3,DISALLOWED],
	 [4,3,2,2,1,DISALLOWED,DISALLOWED,DISALLOWED,3],
	 [3,DISALLOWED,DISALLOWED,DISALLOWED,DISALLOWED,0,0,0,0],
	 [DISALLOWED,4,DISALLOWED,DISALLOWED,DISALLOWED,0,0,0,0],
	 [DISALLOWED,DISALLOWED,3,DISALLOWED,DISALLOWED,0,0,0,0],
	 [DISALLOWED,DISALLOWED,DISALLOWED,3,DISALLOWED,0,0,0,0],
	 [DISALLOWED,DISALLOWED,DISALLOWED,DISALLOWED,4,0,0,0,0]
]

H = {
	'A': { '#0': 0, '#1': 1, '#2': 2, '#3': 2, '#4': 5, '#5': 3, '#6': 999, '#7': 999, '#8': 999},
	'B': { '#0': 2, '#1': 1, '#2': 2, '#3': 2, '#4': 3, '#5': 999, '#6': 5, '#7': 999, '#8': 999},
	'C': { '#0': 2, '#1': 1, '#2': 0, '#3': 0, '#4': 3, '#5': 999, '#6': 999, '#7': 3, '#8': 999},
	'D': { '#0': 4, '#1': 3, '#2': 2, '#3': 2, '#4': 1, '#5': 999, '#6': 999, '#7': 999, '#8': 3},
	'E': { '#0': 3, '#1': 999, '#2': 999, '#3': 999, '#4': 999, '#5': 0, '#6': 0, '#7': 0, '#8': 0},
	'F': { '#0': 999, '#1': 4, '#2': 999, '#3': 999, '#4': 999, '#5': 0, '#6': 0, '#7': 0, '#8': 0},
	'G': { '#0': 999, '#1': 999, '#2': 3, '#3': 999, '#4': 999, '#5': 0, '#6': 0, '#7': 0, '#8': 0},
	'H': { '#0': 999, '#1': 999, '#2': 999, '#3': 3, '#4': 999, '#5': 0, '#6': 0, '#7': 0, '#8': 0},
	'I': { '#0': 999, '#1': 999, '#2': 999, '#3': 999, '#4': 4, '#5': 0, '#6': 0, '#7': 0, '#8': 0},
}

F = {
	'A': { '#0': 0, '#1': 1, '#2': 2, '#3': 2, '#4': 5, '#5': 3},
	'B': { '#0': 2, '#1': 1, '#2': 2, '#3': 2, '#4': 3, '#6': 5},
	'C': { '#0': 2, '#1': 1, '#2': 0, '#3': 0, '#4': 3, '#7': 3},
	'D': { '#0': 4, '#1': 3, '#2': 2, '#3': 2, '#4': 1, '#8': 3},
	'E': { '#0': 3, '#5': 0, '#6': 0, '#7': 0, '#8': 0},
	'F': { '#1': 4, '#5': 0, '#6': 0, '#7': 0, '#8': 0},
	'G': { '#2': 3, '#5': 0, '#6': 0, '#7': 0, '#8': 0},
	'H': { '#3': 3, '#5': 0, '#6': 0, '#7': 0, '#8': 0},
	'I': { '#4': 4, '#5': 0, '#6': 0, '#7': 0, '#8': 0},
}

G = {
	'Ann': {'RB': 3, 'CAM': 2, 'GK': 1},
	'Ben': {'LW': 3, 'S': 2, 'CM': 1},
	'Cal': {'CAM': 3, 'RW': 2, 'SWP': 1},
	'Dan': {'S': 3, 'LW': 2, 'GK': 1},
	'Ela': {'GK': 3, 'LW': 2, 'F': 1},
	'Fae': {'CM': 3, 'GK': 2, 'CAM': 1},
	'Gio': {'GK': 3, 'CM': 2, 'S': 1},
	'Hol': {'CAM': 3, 'F': 2, 'SWP': 1},
	'Ian': {'S': 3, 'RW': 2, 'RB': 1},
	'Jon': {'F': 3, 'LW': 2, 'CB': 1},
	'Kay': {'GK': 3, 'RW': 2, 'LW': 1, 'LB': 0}
}


indexes = m.compute(A)
print_matrix(A, msg='Lowest cost through this matrix:')
total = 0
for row, column in indexes:
    value = A[row][column]
    total += value
    print(f'({row}, {column}) -> {value}')
print(f'total cost: {total}')