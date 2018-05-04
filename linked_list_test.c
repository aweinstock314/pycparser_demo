struct node{
    double value;
    int index;
    struct node* next;
};


struct node a_node;


int tests_that_use_pycparser_ast_main()
{
    struct node * head;
    int i;

    head=&a_node;

    head->value=2.0;
    head->index=3;
    head->next=0;
    
    for (i=0;i<10;i++) 
        head=head->next;


    return 0;
}
