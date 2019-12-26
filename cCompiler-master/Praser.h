#ifndef _PRASER_H_
#define _PRASER_H_
#include "block.h"
#include "tree.h"
#include "innerCode.h"
#include <vector>
#include <set>


using namespace std;

class Praser {
public:

	Praser(gramTree*);	//锟斤拷锟届函锟斤拷
	~Praser();	//锟斤拷锟斤拷锟斤拷锟斤拷

private:
	map<string, funcNode> funcPool;		    	//锟斤拷锟斤拷锟斤拷
	vector<Block> blockStack;				     //维锟斤拷锟斤拷栈
	InnerCode innerCode;					          //锟叫硷拷锟斤拷锟斤拷锟斤拷晒锟斤拷锟�
	//set<string> build_in_function;

	struct gramTree* root;

	void praserInit();
	void praserGramTree(struct gramTree* node);

	
	struct gramTree* praser_declaration(struct gramTree* node);	
	void praser_init_declarator_list(string, struct gramTree*);
	void praser_init_declarator(string, struct gramTree* );			

	struct gramTree* praser_function_definition(struct gramTree*);
	string praser_parameter_list(struct gramTree*,string,bool);			
	string praser_parameter_declaration(struct gramTree*, string,bool);	

	struct gramTree* praser_statement(struct gramTree*);

	void praser_expression_statement(struct gramTree*);
	varNode praser_expression(struct gramTree*);

	string praser_argument_expression_list(struct gramTree*,string);

	void praser_jump_statement(struct gramTree*);
	void praser_compound_statement(struct gramTree*);
	void praser_selection_statement(struct gramTree*);
	void praser_iteration_statement(struct gramTree*);

	varNode praser_assignment_expression(struct gramTree*);			
	varNode praser_logical_or_expression(struct gramTree*);			
	varNode praser_logical_and_expression(struct gramTree*);		
	varNode praser_inclusive_or_expression(struct gramTree*);
	varNode praser_exclusive_or_expression(struct gramTree*);
	varNode praser_and_expression(struct gramTree*);
	varNode praser_equality_expression(struct gramTree*);
	varNode praser_relational_expression(struct gramTree*);
	varNode praser_shift_expression(struct gramTree*);
	varNode praser_additive_expression(struct gramTree*);
	varNode praser_multiplicative_expression(struct gramTree*);
	varNode praser_unary_expression(struct gramTree*);
	varNode praser_postfix_expression(struct gramTree*);
	varNode praser_primary_expression(struct gramTree*);


	string lookupVar(string name);			
	bool lookupCurruntVar(string name);		
	struct varNode lookupNode(string name);	
	string getFuncRType();
	string getArrayType(string);
	struct arrayNode getArrayNode(string);

	int getBreakBlockNumber();

	struct varNode createTempVar(string name, string type);

	void error(int line, string error);

	void print_map();
	void print_code();
};




#endif // !_PRASER_H_