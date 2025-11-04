# Para Windows
CC = gcc
CFLAGS = -Wall -Iinclude
SRC_DIR = codigo
INC_DIR = include
BUILD_DIR = build
TARGET = $(BUILD_DIR)/output.exe

SOURCES = $(wildcard $(SRC_DIR)/*.c)

all:
	if not exist $(BUILD_DIR) mkdir $(BUILD_DIR)
	$(CC) $(CFLAGS) $(SOURCES) -o $(TARGET)
	@echo Executavel criado: $(TARGET)

clean:
	if exist $(BUILD_DIR) rmdir /s /q $(BUILD_DIR)

run: all
	$(TARGET)

.PHONY: all clean run