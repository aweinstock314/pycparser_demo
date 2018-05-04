struct node{
    double value;
    int index;
    struct node* next;
};


struct node a_node;


int tests_that_use_pycparser_ast_main()
{
    struct node * head;
    struct node *tmp;
    int i;

    head=&a_node;

    head->value=2.0;
    head->index=3;
    head->next=0;
    
    for (i=0;i<10;i++) 
        head=head->next;

    head=0;
    for (i=0;i<10;i++) 
    {
        tmp=smalloc(sizeof(struct_node));
        tmp->value=2.0;
        tmp->index=3;
        tmp->next=head;
        head=tmp;
    }

    return 0;
}
