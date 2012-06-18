data_miner: data_miner.o model.o
	gcc data_miner.o model.o -I/usr/local/include \
		-L/usr/local/lib -ligraph -lm -o data_miner

model.o: model.c model.h
	gcc -c model.c 

data_miner.o: data_miner.c model.h
	gcc -c data_miner.c
