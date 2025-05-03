build/test_cria_vetores: src/test_cria_vetores.c src/funcoes.c
	gcc -Iinclude -Wall -O2 -o build/test_cria_vetores src/test_cria_vetores.c src/funcoes.c -lm
build/test_cria_encadeadas: src/test_cria_encadeadas.c src/funcoes.c
	gcc -Iinclude -Wall -O2 -o build/test_cria_encadeadas src/test_cria_encadeadas.c src/funcoes.c -lm
