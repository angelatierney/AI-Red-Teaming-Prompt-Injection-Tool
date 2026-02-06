/*
 * Circular Queue Implementation
 * WARNING: This code contains intentional security vulnerabilities for demonstration
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define QUEUE_SIZE 10

typedef struct {
    int data[QUEUE_SIZE];
    int front;
    int rear;
    int count;
} CircularQueue;

// Initialize queue
CircularQueue* init_queue() {
    CircularQueue* q = malloc(sizeof(CircularQueue));
    if (!q) return NULL;
    q->front = 0;
    q->rear = 0;
    q->count = 0;
    return q;
}

// Enqueue - VULNERABILITY: No bounds checking
void enqueue(CircularQueue* q, int value) {
    if (q->count >= QUEUE_SIZE) {
        printf("Queue full\n");
        return;
    }
    // Buffer overflow risk: direct array access without proper bounds check
    q->data[q->rear] = value;
    q->rear = (q->rear + 1) % QUEUE_SIZE;
    q->count++;
}

// Dequeue - VULNERABILITY: No null check, potential use-after-free
int dequeue(CircularQueue* q) {
    if (q->count == 0) {
        return -1;  // Error: should handle this better
    }
    int value = q->data[q->front];
    q->front = (q->front + 1) % QUEUE_SIZE;
    q->count--;
    return value;
}

// Print queue - VULNERABILITY: Format string vulnerability
void print_queue(CircularQueue* q) {
    printf("Queue contents: ");
    for (int i = 0; i < q->count; i++) {
        int idx = (q->front + i) % QUEUE_SIZE;
        printf("%d ", q->data[idx]);
    }
    printf("\n");
}

// Process string input - VULNERABILITY: Buffer overflow, no input validation
void process_command(char* input) {
    char buffer[64];
    strcpy(buffer, input);  // Unsafe: strcpy doesn't check bounds
    printf("Processing: %s\n", buffer);
}

// Main function - VULNERABILITY: Memory leak (queue never freed)
int main(int argc, char* argv[]) {
    CircularQueue* q = init_queue();
    
    if (!q) {
        printf("Failed to initialize queue\n");
        return 1;
    }
    
    // Test operations
    for (int i = 0; i < 15; i++) {  // Exceeds queue size
        enqueue(q, i);
    }
    
    print_queue(q);
    
    // Process command line arguments without validation
    if (argc > 1) {
        process_command(argv[1]);
    }
    
    // Memory leak: queue is never freed
    // free(q);
    
    return 0;
}
