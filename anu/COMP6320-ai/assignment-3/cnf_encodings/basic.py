# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2018
# Miquel Ramirez Javega, Nathan Robinson, Enrico Scala ({enrico.scala,miquel
# .ramirez}@anu.edu.au)

""" Student Details

    Student Name: Rui Qiu
    Student ID: u6139152
    Email: u6139152@anu.edu.au
    Date: 2018-05-19
"""


""" This file contains the methods you need to implement to create a basic
    (non-split) encoding of planning as SAT.

    You can work your way through the exercises below to build up the encoding.

    We strongly recommend that you test as you go on some of the smaller
    benchmark problems.

    Here is a simple example to run the problem on the smallest Miconics
    instance:

    python3 planner.py benchmarks/miconic/domain.pddl
    benchmarks/miconic/problem01.pddl miconic1 4

    You might want to implement the plan extraction method after you implement
    the method to create the CNF variables. You will then be able to generate
    (probably incorrect) plans as you add more constraints.

    To test the fluent mutex axioms and reachable action axioms you will need
    to turn on the plangraph computation "-p true".

    Remember, it is relatively easy to figure out where you have gone wrong if
    the SAT solver finds invalid plans. For example if the plan validator
    indicates that an action has an unsatisfied precondition, then there is
    probably something wrong with your precondition clauses or your frame
    axioms. However, if the SAT instance is unsatisfiable, then you will likely
    have to start removing constraints to figure out where you went wrong.

    To help you debug your encoding, you can use the argument "-d true" to
    write an annotated CNF file with the clauses you are generating. Warning:
    Looking through this for large problems will be nearly impossible, so test
    on the small instances.

    Sometimes SAT encodings of planning problems can end up BIG because there
    are just so many actions. Either use the argument "-r true" or clear out
    your tmp_files directory periodically and manually.

    This system is designed to run on either Linux or Mac machines. This is
    unavoidable because we need to call and run external grounding and SAT
    solving programs.

    This software will NOT work on Windows. We suggest using a virtual machine,
    or working in the labs if you do not have a linux installation.
"""


from strips_problem import Action, Proposition
from utilities import encoding_error_code

from .encoding_base import Encoding, EncodingException

encoding_class = 'BasicEncoding'


class BasicEncoding(Encoding):
    """ A simple basic encoding along the lines of SatPlan06 with full frame
        axioms.

        Variables and clauses are created once
    """

###############################################################################
#                You need to implement the following methods                  #
###############################################################################

    def make_variables(self, horizon):
        """ Make the variables (state and action fluents) for the problem.

            Exercise 1 - 5 Marks

            The method self.new_cnf_code(step, name, object) will return an int
            representing a new CNF variable for you to use in your encoding.

            Let k be the horizon which is passed as a parameter. Use the above
            method to make one variable for each Proposition at each step 0..k
            and one variable for each Action at each step from 0..k-1.

            Access the actions and propositions from the lists
            self.problem.actions and self.problem.propositions.

            Use str(proposition) to get name of a proposition and str(action)
            to get the name of an action when calling self.new_cnf_code.

            For object, you should just pass either the Proposition or Action
            object.

            So, self.new_cnf_code(4, str(a), a) will create a new variable and
            return a code (an int) representing the CNF variable for action a,
            at step 4.

            Since you will need to use these variables to make your constraints
            later, you should store them in self.action_fluent_codes and
            self.proposition_fluent_codes.

            These should map each (Action, step) pair and each (Proposition,
            step) pair to the appropriate code.

            Once you have made the variables, you can get the step, name, and
            object (Action or Proposition) with the following:
               - self.cnf_code_steps[code]
               - self.cnf_code_names[code]
               - self.cnf_code_objects[code]

            You shouldn't need to use these until you come to extract the plan
            generated by the SAT solver, but they might be useful for
            debugging!

            (BasicEncoding, int) -> None
        """
        self.action_fluent_codes = {}
        self.proposition_fluent_codes = {}

        """ YOUR CODE HERE """

        for a in self.problem.actions:
            for t in range(0, horizon):
                code = self.new_cnf_code(t, str(a), a)
                self.action_fluent_codes[(a, t)] = code

        for p in self.problem.propositions:
            for t in range(0, horizon+1):
                code = self.new_cnf_code(t, str(p), p)
                self.proposition_fluent_codes[(p, t)] = code

    def make_initial_state_and_goal_axioms(self, horizon):
        """ Make clauses representing the initial state and goal.

            Exercise 2 - 5 Marks

            In this method, add clauses to the encoding which ensure that the
            initial state of the problem holds at step 0. The Propostions which
            must be true are in self.problem.pos_initial_state and the
            Propositions which must be false are in
            self.problem.neg_initial_state.

            Every Proposition in the problem will be in one of these two sets.

            Also add clauses which ensure that the goal holds at the horizon.
            Similarly to the start state, the goal clauses are in
            self.problem.goal.

            Not every Proposition will be in the goal. The truth values of
            other Propositions should remain unconstrained.

            A clause is a list of positive or negative integers (representing
            positive and negative literals) using the variables you created
            for Q1. Get the variables from self.proposition_fluent_codes).

            Every clause has a type, which is represented by a string.

            Add clauses to the encoding with self.add_clause(clause,
            clause_type).

            The type of the start state clauses should be "start" and the type
            of the goal clauses should be "goal".

            (BasicEncoding, int) -> None
        """

        """ *** YOUR CODE HERE *** """

        for p in self.problem.propositions:
            if p in self.problem.pos_initial_state:
                self.add_clause([self.proposition_fluent_codes[(p, 0)]],
                                "start")
            if p in self.problem.neg_initial_state:
                self.add_clause([-self.proposition_fluent_codes[(p, 0)]],
                                "start")
            if p in self.problem.goal:
                self.add_clause([self.proposition_fluent_codes[(p, horizon)]],
                                "goal")

    def make_precondition_and_effect_axioms(self, horizon):
        """ Make clauses representing action preconditions and effects.

            Exercise 3 - 5 Marks

            In this method, add clauses to the encoding which ensure that
            If an action is executed at step t = 0..k-1:
                - its preconditions hold at step t and
                - its effects hold at step t+1.
                    (No action will both add and delete the same proposition)

            Add clauses with self.add_clause(clause, clause_type).

            In your clauses use the variables from self.action_fluent_codes and
            self.proposition_fluent_codes.

            Precondition clauses have the type 'pre' and effect clauses have
            the type "eff".

            Don't forget to look in strips_problem.py for the data structures
            you need to use!

            (BasicEncoding, int) -> None
        """

        """ *** YOUR CODE HERE *** """

        # PRE_EFF_COUNT = 0

        for a in self.problem.actions:
            for t in range(0, horizon):
                for pre in a.preconditions:
                    precond_clause = list()
                    precond_clause.append(-self.action_fluent_codes[(a, t)])
                    precond_clause.append(
                        self.proposition_fluent_codes[(pre, t)])
                    self.add_clause(precond_clause, "pre")
                    # PRE_EFF_COUNT += 1

                for eff in list(set(a.pos_effects) ^ set(a.neg_effects)):
                    # use set operator to exclude action that both adds and
                    # deletes the same proposition
                    effect_clause = list()
                    effect_clause.append(-self.action_fluent_codes[(a, t)])
                    if eff in a.pos_effects:
                        effect_clause.append(
                            self.proposition_fluent_codes[(eff, t + 1)])
                    else:
                        effect_clause.append(
                            -self.proposition_fluent_codes[(eff, t + 1)])
                    self.add_clause(effect_clause, "eff")
                    # PRE_EFF_COUNT += 1

        # print("PRE_EFF_COUNT:")
        # print(PRE_EFF_COUNT)

    def make_explanatory_frame_axioms(self, horizon):
        """ Make clauses representing explanatory frame axioms.

            Exercise 4 - 10 Marks

            In this method, add clauses to the encoding which ensure that
            If a proposition p is true at step t = 1..k:
                - either p is true at t-1 or
                - an action is executed at t-1 which added p.

            If a proposition p is false at step t = 1..k:
                - either p is false at t-1 or
                - an action is executed at t-1 which deletes p

            Add clauses with self.add_clause(clause, clause_type).

            In your clauses use the variables from self.action_fluent_codes
            and self.proposition_fluent_codes.

            These clauses have the type "frame".

            To make this process easier, Proposition objects have lists of
            the actions
            which have them as positive and negative and effects.

            (BasicEncoding, int) -> None
        """

        """ *** YOUR CODE HERE *** """

        # FRAME_COUNT = 0

        for p in self.problem.propositions:
            for t in range(0, horizon):
                clause1 = list()
                clause2 = list()

                clause1.append(self.proposition_fluent_codes[(p, t)])
                clause1.append(-self.proposition_fluent_codes[(p, t + 1)])
                for a in p.pos_effects:
                    clause1.append(self.action_fluent_codes[(a, t)])

                clause2.append(-self.proposition_fluent_codes[(p, t)])
                clause2.append(self.proposition_fluent_codes[(p, t + 1)])
                for a in p.neg_effects:
                    clause2.append(self.action_fluent_codes[(a, t)])

                self.add_clause(clause1, "frame")
                self.add_clause(clause2, "frame")
                # FRAME_COUNT += 2

        # print("FRAME COUNT:")
        # print(FRAME_COUNT)

    def make_serial_mutex_axioms(self, horizon):
        """ Make clauses representing serial mutex.

            Exercise 5 - 10 Marks

            In this method, add clauses to the encoding which ensure that at
            most one action is executed at each step t = 0..k. (It could be the
            case that no actions are executed at some steps).

            To get full marks, you should add as few clauses as possible.
            Notice that actions with conflicting effects are already prevented
            from being executed in parallel.

            Add clauses with self.add_clause(clause, clause_type).

            In your clauses use the variables from self.action_fluent_codes.

            These clauses have the type "mutex".

            (BasicEncoding, int) -> None
        """

        """ *** YOUR CODE HERE *** """

        # SE_MUTEX_COUNT = 0

        # here also use set operation to exclude actions that cause
        # conflicting effects

        consistent_actions = self.problem.actions
        for a in consistent_actions:
            if set(a.pos_effects) & set(a.neg_effects) != set():
                consistent_actions.remove(a)

        for a1 in consistent_actions:
            for a2 in consistent_actions:
                for t in range(0, horizon):
                    if a1 != a2:
                        mutex_clause = list()
                        mutex_clause.append(-self.action_fluent_codes[(a1, t)])
                        mutex_clause.append(-self.action_fluent_codes[(a2, t)])
                        self.add_clause(mutex_clause, "mutex")
                        # SE_MUTEX_COUNT += 1

        # print("SERIAL MUTEX COUNT:")
        # print(SE_MUTEX_COUNT)

    def make_interference_mutex_axioms(self, horizon):
        """ Make clauses preventing interfering actions from being executed
            in parallel.

            Exercise 6 - 10 Marks

            In this method, add clauses to the encoding which ensure that two
            actions cannot be executed in parallel at a step t == 0..k if they
            interfere.

            Two actions a1 and a2 interfere if there is a Proposition p such
            that p in EFF-(a1) and p in PRE(a2).

            To get full marks, you should not add clauses for interfering
            actions if their parallel execution is already prevented by
            conflict due to effect clauses. Also, careful not to add duplicate
            clauses!

            If you find your encoding time to be slow, it might be due to an
            inefficient implementation of this function. As a hint to make it
            faster, make use of the `neg_effects` and `preconditions`
            attributes stored in Proposition objects, instead of the
            `neg_effects` and `preconditions` attributes in Action objects.

            Add clauses with self.add_clause(clause, clause_type).

            In your clauses use the variables from self.action_fluent_codes.

            These clauses have the type "mutex".

            (BasicEncoding, int) -> None
        """

        """ *** YOUR CODE HERE *** """

        # INT_MUTEX_COUNT = 0

        consistent_actions = self.problem.actions
        for a in consistent_actions:
            if set(a.pos_effects) & set(a.neg_effects) != set():
                consistent_actions.remove(a)

        # use this hashable data type to store what has been added
        actions_dict = dict()
        for a1 in consistent_actions:
            for a2 in consistent_actions:
                for t in range(0, horizon):
                    # note that a1 and a2 can be mutually switched,
                    # here we should check for (a1, a2) if (a2, a1) is already
                    # in the dictionary above...
                    if (a2, a1, t) not in actions_dict.keys() and a1 != a2:
                        for p in self.problem.propositions:
                            # if a1 in p.neg_effects and a2 in p.preconditions:
                            if a1 in p.neg_effects and a2 in p.preconditions:
                                mutex_clause = list()
                                mutex_clause.append(
                                    -self.action_fluent_codes[(a1, t)])
                                mutex_clause.append(
                                    -self.action_fluent_codes[(a2, t)])
                                mutex_clause.append(
                                    -self.proposition_fluent_codes[(p, t)])
                                self.add_clause(mutex_clause, "mutex")
                                # add to our dictionary to keep track of
                                # added combinations
                                actions_dict[(a1, a2, t)] = 1
                                # INT_MUTEX_COUNT += 1

        # print("INT MUTEX COUNT:")
        # print(INT_MUTEX_COUNT)

    def make_reachable_action_axioms(self, horizon):
        """ Make unit clauses preventing actions from being executed before they
            become available in the plangraph.

            Exercise 7 - 5 Marks

            In this method, add clauses to the encoding which ensure that an
            action is not executed before the first step it is available in
            self.problem.action_first_step.

            For example, if self.problem.action_first_step[action1] == 5, then
            you would introduce clauses stopping action1 from being executed at
            steps 0..4.

            These clauses are not required for correctness, but may improve
            performance.

            Add clauses with self.add_clause(clause, clause_type).

            In your clauses use the variables from self.action_fluent_codes.

            These clauses have the type "reach".

            (BasicEncoding, int) -> None
        """

        """ *** YOUR CODE HERE *** """

        # a@t -> not a@t-1 and not a@t-2 ...
        # (not a@t or not a@t-1) and (...) and (...)...

        # REACH_COUNT = 0

        for a in self.problem.actions:
            threshold = min(self.problem.action_first_step[a], horizon)
            # when we set horizon as ramp, could start from the bottom and have
            # horizon < first_step
            for t in range(0, threshold):
                self.add_clause([-self.action_fluent_codes[(a, t)]], "reach")
                # REACH_COUNT += 1

        # print("REACH COUNT:")
        # print(REACH_COUNT)

    def make_fluent_mutex_axioms(self, horizon):
        """ Make clauses representing fluent mutex as computed by the
            plangraph.

            Exercise 8 - 5 Marks

            In this method, add clauses to the encoding which ensure that pairs
            of propositions cannot both be true at the same time. These
            constraints are computed when the plangraph is generated.

            These clauses are not required for correctness, but usually make
            planning faster by causing the SAT solver to backtrack earlier.

            The dictionary self.problem.fluent_mutex maps integers representing
            planning steps to lists of proposition mutex relationships at each
            step from 1...n, where n is the step that the plangraph levels off.
            Note that the dictionary doesn't contain steps greater than n,
            because the relationships at step n also hold for every step
            greater than n. Thus you can get those mutex relationships by
            querying the dictionary with step n.

            You can get n by getting the largest key in
            self.problem.fluent_mutex maps.

            It is possible that the current horizon is less than n. In this
            case, mutex relationships larger than the horizon should, of
            course, be ignored.

            As the initial state clauses completely determine the truth values
            of fluents at step 0, there is no need for fluent mutex clauses
            there.

            Each list of mutex relationships in self.problem.fluent_mutex will
            be as follows:

              [(f1, f2), ....]

            Say, we have (f1, f2), then there should be a clause [-f1, -f2]
            (obviously substituting the appropriate CNF codes for f1 and f2,
            depending on the step.

            Add clauses with self.add_clause(clause, clause_type).

            In your clauses use the variables from
            self.proposition_fluent_codes.

            These clauses have the type "fmutex".

            (BasicEncoding, int) -> None
        """

        """ *** YOUR CODE HERE *** """

        # FMUTEX_COUNT = 0

        n = max(self.problem.fluent_mutex.keys())
        ceiling = min(n, horizon)
        # this step is probably redundant, since the max key step is determined
        # by t, and t in the very beginning is bounded by horizon, then we
        # probably won't have n > horizon.
        # but we still keep it here anyways.

        for t in range(1, ceiling+1):
            mutex_rlshp = self.problem.fluent_mutex[t]
            for mpair in mutex_rlshp:
                clause = list()
                clause.append(-self.proposition_fluent_codes[(mpair[0], t)])
                clause.append(-self.proposition_fluent_codes[(mpair[1], t)])
                self.add_clause(clause, "fmutex")
                # FMUTEX_COUNT += 1

        # print("FMUTEX COUNT:")
        # print(FMUTEX_COUNT)

    def build_plan(self, horizon):
        """Build a plan from the true variables in a satisfying valuation found
           by the SAT solver.

           Exercise 9 - 5 marks

           self.true_vars is a set with the codes of the CNF variables which
           the SAT solver has set to true in the satisfying valuation it found.

           You can get the step, name, and object (Action/Proposition) of
           each variable (state or action fluent) with:
               - self.cnf_code_steps[code]
               - self.cnf_code_names[code]
               - self.cnf_code_objects[code]

           You can check if an object is an Action or Proposition with
               - isinstance(obj, Action) and
               - isinstance(obj, Proposition)

           You should add the plan to self.plan, which has the structure
           [action_list, action_list, ...].

           For each step t = 0..k-1, it has a (possibly empty) list of the
           actions which were executed at that step.

           So, if we have a0 and a1 at step 0 and a2 at step 2, then self.plan
           will be:

               [[a0, a1], [], [a2]]

           where a0, a1, a2, etc. are Action objects (not just their names).

           The system will validate the plans you generate, so make sure you
           test your encodings on a number of different problems.

           (BasicEncoding, int) -> None
        """
        self.plan = []

        """ *** YOUR CODE HERE *** """

        self.plan = list(list() for i in range(horizon))  # list of lists
        truths = self.true_vars
        for something in truths:
            obj = self.cnf_code_objects[something]
            if isinstance(obj, Action):
                steps = self.cnf_code_steps[something]
                self.plan[steps].append(obj)


###############################################################################
#                    Do not change the following method                       #
###############################################################################

    def encode(self, horizon, exec_semantics, plangraph_constraints):
        """ Make an encoding of self.problem for the given horizon.

            For this encoding, we have broken this method up into a number
            of sub-methods that you need to implement.

           (BasicEncoding, int, str, str) -> None
        """

        self.make_variables(horizon)

        self.make_initial_state_and_goal_axioms(horizon)

        self.make_precondition_and_effect_axioms(horizon)

        self.make_explanatory_frame_axioms(horizon)

        if exec_semantics == "serial":
            self.make_serial_mutex_axioms(horizon)
        elif exec_semantics == "parallel":
            self.make_interference_mutex_axioms(horizon)
        else:
            assert False

        if self.problem.fluent_mutex is not None:
            # These constraints will only be included if the plangraph was
            # computed
            if plangraph_constraints == "both":
                self.make_reachable_action_axioms(horizon)
                self.make_fluent_mutex_axioms(horizon)
            elif plangraph_constraints == "fmutex":
                self.make_fluent_mutex_axioms(horizon)
            elif plangraph_constraints == "reachable":
                self.make_reachable_action_axioms(horizon)
