/*
 * Circular Queue Implementation - SECURE VERSION
 * Refactored with security best practices
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>

#define QUEUE_SIZE 10
#define MAX_INPUT_SIZE 256

typedef struct {
    int data[QUEUE_SIZE];
    int front;
    int rear;
    int count;
} CircularQueue;

// Initialize queue with proper error handling
CircularQueue* init_queue() {
    CircularQueue* q = calloc(1, sizeof(CircularQueue));  // Use calloc for zero-initialization
    if (!q) {
        fprintf(stderr, "Error: Failed to allocate memory for queue\n");
        return NULL;
    }
    q->front = 0;
    q->rear = 0;
    q->count = 0;
    return q;
}

// Free queue memory - FIXED: Added proper cleanup
void free_queue(CircularQueue* q) {
    if (q) {
        free(q);
    }
}

// Enqueue with proper bounds checking - FIXED: Added validation
bool enqueue(CircularQueue* q, int value) {
    if (!q) {
        fprintf(stderr, "Error: Null queue pointer\n");
        return false;
    }
    
    // Check for integer overflow
    if (value > INT_MAX || value < INT_MIN) {
        fprintf(stderr, "Error: Value out of range\n");
        return false;
    }
    
    if (q->count >= QUEUE_SIZE) {
        fprintf(stderr, "Queue full\n");
        return false;
    }
    
    // Safe array access with bounds checking
    if (q->rear < 0 || q->rear >= QUEUE_SIZE) {
        fprintf(stderr, "Error: Invalid rear index\n");
        return false;
    }
    
    q->data[q->rear] = value;
    q->rear = (q->rear + 1) % QUEUE_SIZE;
    q->count++;
    return true;
}

// Dequeue with proper error handling - FIXED: Added null checks
bool dequeue(CircularQueue* q, int* value) {
    if (!q || !value) {
        fprintf(stderr, "Error: Null pointer\n");
        return false;
    }
    
    if (q->count == 0) {
        fprintf(stderr, "Queue empty\n");
        return false;
    }
    
    // Safe array access
    if (q->front < 0 || q->front >= QUEUE_SIZE) {
        fprintf(stderr, "Error: Invalid front index\n");
        return false;
    }
    
    *value = q->data[q->front];
    q->front = (q->front + 1) % QUEUE_SIZE;
    q->count--;
    return true;
}

// Print queue - FIXED: Removed format string vulnerability
void print_queue(CircularQueue* q) {
    if (!q) {
        fprintf(stderr, "Error: Null queue pointer\n");
        return;
    }
    
    printf("Queue contents: ");
    for (int i = 0; i < q->count; i++) {
        int idx = (q->front + i) % QUEUE_SIZE;
        if (idx >= 0 && idx < QUEUE_SIZE) {
            printf("%d ", q->data[idx]);
        }
    }
    printf("\n");
}

// Process string input - FIXED: Safe string handling with bounds checking
bool process_command(const char* input) {
    if (!input) {
        fprintf(stderr, "Error: Null input pointer\n");
        return false;
    }
    
    size_t input_len = strnlen(input, MAX_INPUT_SIZE);
    if (input_len >= MAX_INPUT_SIZE) {
        fprintf(stderr, "Error: Input too long\n");
        return false;
    }
    
    // Use stack buffer with proper size
    char buffer[MAX_INPUT_SIZE];
    
    // Safe copy with bounds checking
    if (strncpy(buffer, input, MAX_INPUT_SIZE - 1) == NULL) {
        fprintf(stderr, "Error: Failed to copy input\n");
        return false;
    }
    buffer[MAX_INPUT_SIZE - 1] = '\0';  // Ensure null termination
    
    printf("Processing: %s\n", buffer);
    return true;
}

// Main function - FIXED: Proper memory management and input validation
int main(int argc, char* argv[]) {
    CircularQueue* q = init_queue();
    
    if (!q) {
        fprintf(stderr, "Failed to initialize queue\n");
        return 1;
    }
    
    // Test operations with bounds checking
    for (int i = 0; i < QUEUE_SIZE; i++) {  // FIXED: Don't exceed queue size
        if (!enqueue(q, i)) {
            fprintf(stderr, "Failed to enqueue %d\n", i);
            break;
        }
    }
    
    print_queue(q);
    
    // Process command line arguments with validation
    if (argc > 1) {
        if (!process_command(argv[1])) {
            fprintf(stderr, "Failed to process command\n");
        }
    }
    
    // FIXED: Properly free memory before exit
    free_queue(q);
    
    return 0;
}
