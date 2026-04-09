import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("square", type=int, help="display the square of a given number")
# parser.add_argument(
#     "-v", "--verbose", help="Increase output verbosity", type=int, choices=[0, 1, 2]
# )


# args = parser.parse_args()

# answer = args.square**2

# if args.verbose == 2:
#     print(f"The square of {args.square} is {answer}")
# elif args.verbose == 1:
#     print(f"{args.square}^2 = {answer}")
# else:
#     print(answer)


# One step further
# parser = argparse.ArgumentParser()

# parser.add_argument("square", help="Display the squre of the number", type=int)
# parser.add_argument(
#     "-v", "--verbose", help="Increase output verbosity", action="count", default=0
# )


# args = parser.parse_args()
# answer = args.square**2

# if args.verbose >= 2:
#     print(f"The square of {args.square} is {answer}")
# elif args.verbose >= 1:
#     print(f"{args.square}^2 = {answer}")
# else:
#     print(answer)


# Another step further
parser = argparse.ArgumentParser()

parser.add_argument("x", help="the base", type=int)
parser.add_argument("y", help="the exponent", type=int)
parser.add_argument(
    "-v", "--verbose", help="increases output verbosity", action="count", default=0
)

args = parser.parse_args()
answer = args.x**args.y

if args.verbose >= 2:
    print(f"Running {__file__.split("/")[-1]}\n")
    print(f"{args.x}^{args.y} = {answer}")
elif args.verbose >= 1:
    print(f"{args.x}^{args.y} = {answer}")
else:
    print(answer)
