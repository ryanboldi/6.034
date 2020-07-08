from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    #check through all the rules, see if their consequents match the hypothesis,
    #could use match(pattern, datum) to match the rules' consequents (rule.consequent) to one of the hypotheses.
    #if they do, populate antecedent and add to goal tree
    #they are either a leaf or a rule expression, 
    #keep backchaining untill we get a full goal tree
    goal_tree = OR(hypothesis)
    #we want a whole nested statement that tells us whether or not the hypothesis is true.
    for i in rules:
        for c in i.consequent():
            matchBinds = match(c, hypothesis) #if the consequent of any of the rules matches
            if matchBinds != None:
                #figure out if i's antecedent is AND or OR or none
                goal_tree.append(populate(i.antecedent(), matchBinds)) #populate all of its antecedents, and add them to our goal tree

    try:
        goal_tree[1]
    except IndexError:
        pass
        #print "Didn't add anything"
    else:
        print(goal_tree)
        for l in range(1, len(goal_tree)):
            if (isinstance(goal_tree[l], str)):
                goal_tree[l] = backchain_to_goal_tree(rules, goal_tree[l])
            else:
                for g in range(len(goal_tree[l])):
                    #check all the rules we just added
                    #replace the goals with a backchain to goal tree
                    goal_tree[l][g] = simplify(backchain_to_goal_tree(rules, goal_tree[l][g])) 

    return simplify(goal_tree)

# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
