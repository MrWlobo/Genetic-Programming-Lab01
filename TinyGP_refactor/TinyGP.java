/*
 * Program:   tiny_gp.java
 *
 * Author:
 *
 */

import java.util.*;
import java.io.*;
import java.util.List;
import java.util.ArrayList;

public class TinyGP {
    List<Double> fitness;
    List<List<Character>> pop;

    Random rd = new Random();
    final int
            ADD = 110,
            SUB = 111,
            MUL = 112,
            DIV = 113,
            FSET_START = ADD,
            FSET_END = DIV;

    List<Double> x = new ArrayList<>();

    double minrandom, maxrandom;
    List<Character> program;
    int PC;
    int varnumber, fitnesscases, randomnumber;
    double fbestpop = 0.0, favgpop = 0.0;
    long seed;
    double avg_len;
    final int
            MAX_LEN = 10000,
            POPSIZE = 100000,
            DEPTH   = 5,
            GENERATIONS = 100,
            TSIZE = 2;
    public final double
            PMUT_PER_NODE  = 0.05,
            CROSSOVER_PROB = 0.9;
    List<List<Double>> targets;

    double run() { /* Interpreter */
        char primitive = program.get(PC++);
        if ( primitive < FSET_START )
            return x.get(primitive);
        switch ( primitive ) {
            case ADD : return run() + run();
            case SUB : return run() - run();
            case MUL : return run() * run();
            case DIV : {
                double num = run(), den = run();
                if ( Math.abs( den ) <= 0.001 ) {
                    return num;
                }
                else {
                    return num / den;
                }
            }
        }
        return 0.0; // should never get here
    }

    int traverse( List<Character> buffer, int buffercount ) {
        if ( buffer.get(buffercount) < FSET_START )
            return ++buffercount;

        return switch (buffer.get(buffercount)) {
            case ADD, SUB, MUL, DIV -> traverse(buffer, traverse(buffer, ++buffercount));
            default -> 0;
        };
    }

    void setup_fitness(String fname) {
        try (java.util.Scanner fileScanner = new java.util.Scanner(new java.io.File(fname))) {

            if (!fileScanner.hasNextLine()) {
                throw new Exception("Data file is empty.");
            }
            
            varnumber = fileScanner.nextInt();
            randomnumber = fileScanner.nextInt();
            minrandom = fileScanner.nextDouble();
            maxrandom = fileScanner.nextDouble();
            fitnesscases = fileScanner.nextInt();

            if (fileScanner.hasNextLine()) {
                fileScanner.nextLine();
            }

            targets = new ArrayList<>();
            final int columns = varnumber + 1;

            if (varnumber + randomnumber >= FSET_START) {
                System.out.println("too many variables and constants");
            }

            for (int i = 0; i < fitnesscases; i++) {
                if (!fileScanner.hasNextLine()) {
                    throw new Exception("Incomplete data file: expected " + fitnesscases + " cases.");
                }

                String line = fileScanner.nextLine();

                // Split the line by one or more whitespace characters
                String[] tokens = line.trim().split("\\s+");

                if (tokens.length < columns) {
                    throw new Exception("Data format error on line " + (i + 1) + ": too few values.");
                }

                targets.add(new ArrayList<>());
                for (int j = 0; j < columns; j++) {
                    targets.get(i).add(Double.parseDouble(tokens[j]));
                }
            }
        }
        catch (FileNotFoundException e) {
            System.out.println("ERROR: Please provide a data file");
            System.exit(0);
        }
        catch (Exception e) {
            System.out.println("ERROR: Incorrect data format. " + e.getMessage());
            System.out.println("Details: " + e.getClass().getName());
            System.exit(0);
        }
    }

    double fitness_function( List<Character> Prog ) {
        int i;
        double result, fit = 0.0;

        for (i = 0; i < fitnesscases; i ++ ) {
            for (int j = 0; j < varnumber; j ++ )
                x.set(j, targets.get(i).get(j));
            program = Prog;
            PC = 0;
            result = run();
            if (!Double.isNaN(Math.abs( result - targets.get(i).get(varnumber)))){
                fit += Math.abs( result - targets.get(i).get(varnumber));
            } else {
                fit = Double.MAX_VALUE;
            }
        }

        return -fit;
    }

    int grow( List<Character> buffer, int pos, int max, int depth ) {
        char prim = (char) rd.nextInt(2);
        int one_child;

        if ( pos >= max )
            return -1;

        if ( pos == 0 )
            prim = 1;

        if ( prim == 0 || depth == 0 ) {
            prim = (char) rd.nextInt(varnumber + randomnumber);
            buffer.set(pos, prim);
            return pos+1;
        }
        else  {
            prim = (char) (rd.nextInt(FSET_END - FSET_START + 1) + FSET_START);
            switch(prim) {
                case ADD:
                case SUB:
                case MUL:
                case DIV:
                    buffer.set(pos, prim);
                    one_child = grow( buffer, pos+1, max,depth-1);
                    if ( one_child < 0 )
                        return -1;
                    return grow( buffer, one_child, max,depth-1 );
            }
        }
        return 0; // should never get here
    }

    int print_indiv( List<Character> buffer, int buffercounter ) {
        int a1, a2;
        if ( buffer.get(buffercounter) < FSET_START ) {
            if ( buffer.get(buffercounter) < varnumber )
                System.out.print( "X"+ (buffer.get(buffercounter) + 1 )+ " ");
            else
                System.out.print( x.get(buffer.get(buffercounter)));
            return ++buffercounter;
        }
        switch(buffer.get(buffercounter)) {
            case ADD: System.out.print( "(");
                a1=print_indiv( buffer, ++buffercounter );
                System.out.print( " + ");
                a2=print_indiv( buffer, a1 );
                System.out.print( ")");
                return a2;
            case SUB: System.out.print( "(");
                a1=print_indiv( buffer, ++buffercounter );
                System.out.print( " - ");
                a2=print_indiv( buffer, a1 );
                System.out.print( ")");
                return a2;
            case MUL: System.out.print( "(");
                a1=print_indiv( buffer, ++buffercounter );
                System.out.print( " * ");
                a2=print_indiv( buffer, a1 );
                System.out.print( ")");
                return a2;
            case DIV: System.out.print( "(");
                a1=print_indiv( buffer, ++buffercounter );
                System.out.print( " / ");
                a2=print_indiv( buffer, a1 );
                System.out.print( ")");
                return a2;
        }

        return 0;
    }


    List<Character> buffer = new ArrayList<>(MAX_LEN);

    List<Character> create_random_indiv( int depth ) {
        List<Character> ind;
        int len;

        do len = grow(buffer, 0, MAX_LEN, depth);
        while (len < 0);

        ind = new ArrayList<>(buffer.subList(0, len));

        return ind;
    }

    List<List<Character>> create_random_pop(int n, int depth) {
        List<List<Character>> pop = new ArrayList<>();


        for (int i = 0; i < n; i ++ ) {
            pop.add(i, create_random_indiv( depth ));
            fitness.add(i, fitness_function( pop.get(i) ));
        }
        return pop;
    }


    void stats( List<Double> fitness, List<List<Character>> pop, int gen ) {
        int i, best = rd.nextInt(POPSIZE);
        int node_count = 0;
        fbestpop = fitness.get(best);
        favgpop = 0.0;

        for ( i = 0; i < POPSIZE; i ++ ) {
            node_count +=  traverse( pop.get(i), 0 );
            favgpop += fitness.get(i);
            if ( fitness.get(i) > fbestpop ) {
                best = i;
                fbestpop = fitness.get(i);
            }
        }
        avg_len = (double) node_count / POPSIZE;
        favgpop /= POPSIZE;
        System.out.print("Generation="+gen+" Avg Fitness="+(-favgpop)+
                " Best Fitness="+(-fbestpop)+" Avg Size="+avg_len+
                "\nBest Individual: ");
        print_indiv( pop.get(best), 0 );
        System.out.print( "\n");
        System.out.flush();
    }

    int tournament( List<Double> fitness, int tsize ) {
        int best = rd.nextInt(POPSIZE), i, competitor;
        double  fbest = Double.MIN_VALUE;

        for ( i = 0; i < tsize; i ++ ) {
            competitor = rd.nextInt(POPSIZE);
            if ( fitness.get(competitor) > fbest ) {
                fbest = fitness.get(competitor);
                best = competitor;
            }
        }
        return best;
    }

    int negative_tournament( List<Double> fitness, int tsize ) {
        int worst = rd.nextInt(POPSIZE), i, competitor;
        double fworst = Double.MAX_VALUE;

        for ( i = 0; i < tsize; i ++ ) {
            competitor = rd.nextInt(POPSIZE);
            if ( fitness.get(competitor) < fworst ) {
                fworst = fitness.get(competitor);
                worst = competitor;
            }
        }
        return worst;
    }

    List<Character> crossover( List<Character> parent1, List<Character> parent2 ) {
        int xo1start, xo1end, xo2start, xo2end;
        List<Character> offspring;

        int len1 = traverse( parent1, 0 );
        int len2 = traverse( parent2, 0 );

        xo1start = rd.nextInt(len1);
        int xo1end_raw = traverse(parent1, xo1start);
        xo1end = Math.min(xo1end_raw, parent1.size());

        xo2start = rd.nextInt(len2);
        int xo2end_raw = traverse(parent2, xo2start);
        xo2end = Math.min(xo2end_raw, parent2.size());


        offspring = new ArrayList<>();

        offspring.addAll(parent1.subList(0, Math.min(xo1start, parent1.size())));
        offspring.addAll(parent2.subList(xo2start, Math.min(xo2end, parent2.size())));
        offspring.addAll(parent1.subList(xo1end, parent1.size()));

        return offspring;
    }

    List<Character> mutation( List<Character> parent, double pmut ) {
        List<Character> parentcopy = new ArrayList<>(parent);

        int i = 0;
        while (i < parentcopy.size()) {
            if ( rd.nextDouble() < pmut ) {
                int mutsite = i;
                char old_node = parentcopy.get(mutsite);

                if ( old_node < FSET_START ) {
                    parentcopy.set(mutsite, (char) rd.nextInt(varnumber + randomnumber));
                    i++;
                } else {
                    int old_subtree_end = traverse(parentcopy, mutsite);

                    List<Character> new_subtree_temp = new ArrayList<>(Collections.nCopies(MAX_LEN, ' '));
                    int new_len = grow(new_subtree_temp, 0, MAX_LEN, 2);

                    if (new_len < 0) {
                        i++;
                        continue;
                    }

                    List<Character> new_subtree = new_subtree_temp.subList(0, new_len);

                    List<Character> head = parentcopy.subList(0, mutsite);

                    List<Character> tail = parentcopy.subList(
                            old_subtree_end,
                            parentcopy.size()
                    );

                    List<Character> new_individual = new ArrayList<>();
                    new_individual.addAll(head);
                    new_individual.addAll(new_subtree);
                    new_individual.addAll(tail);


                    parentcopy = new_individual;

                    i = mutsite + new_len;

                    continue;
                }
            }
            i++;
        }
        return parentcopy;
    }

    void print_parms() {
        System.out.print("-- TINY GP (Java version) --\n");
        System.out.print("SEED="+seed+"\nMAX_LEN="+MAX_LEN+
                "\nPOPSIZE="+POPSIZE+"\nDEPTH="+DEPTH+
                "\nCROSSOVER_PROB="+CROSSOVER_PROB+
                "\nPMUT_PER_NODE="+PMUT_PER_NODE+
                "\nMIN_RANDOM="+minrandom+
                "\nMAX_RANDOM="+maxrandom+
                "\nGENERATIONS="+GENERATIONS+
                "\nTSIZE="+TSIZE+
                "\n----------------------------------\n");
    }

    public TinyGP( String fname, long s ) {
        fitness =  new ArrayList<>();
        seed = s;
        buffer.addAll(Collections.nCopies(MAX_LEN, ' '));

        if ( seed >= 0 )
            rd.setSeed(seed);

        setup_fitness(fname);

        for ( int i = 0; i < FSET_START; i ++ )
            x.add((maxrandom-minrandom)*rd.nextDouble()+minrandom);

        pop = create_random_pop(POPSIZE, DEPTH);
    }

    void evolve() {
        int gen, indivs, offspring, parent1, parent2, parent;
        double newfit;
        List<Character> newind;
        print_parms();
        stats( fitness, pop, 0 );
        for ( gen = 1; gen < GENERATIONS; gen ++ ) {
            if (  fbestpop > -1e-5 ) {
                System.out.print("PROBLEM SOLVED\n");
                System.exit( 0 );
            }
            for ( indivs = 0; indivs < POPSIZE; indivs ++ ) {
                if ( rd.nextDouble() < CROSSOVER_PROB  ) {
                    parent1 = tournament( fitness, TSIZE );
                    parent2 = tournament( fitness, TSIZE );
                    newind = crossover( pop.get(parent1),pop.get(parent2) );
                }
                else {
                    parent = tournament( fitness, TSIZE );
                    newind = mutation( pop.get(parent), PMUT_PER_NODE );
                }
                newfit = fitness_function( newind );
                offspring = negative_tournament( fitness, TSIZE );
                pop.set(offspring, newind);
                fitness.set(offspring, newfit);
            }
            stats( fitness, pop, gen );
        }
        System.out.print("PROBLEM *NOT* SOLVED\n");
        System.exit( 1 );
    }

    public static void main(String[] args) {
        String fname = "src/problem.dat";
        long s = -1;

        if ( args.length == 2 ) {
            s = Integer.parseInt(args[0]);
            fname = args[1];
        }
        if ( args.length == 1 ) {
            fname = args[0];
        }

        TinyGP gp = new TinyGP(fname, s);
        gp.evolve();
    }
}
