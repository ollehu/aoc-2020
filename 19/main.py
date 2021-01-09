""" Solution to the 19th AOC of 2020. """

import re

from sys import argv


def parse_input(lines):
    """
    Parse the lines into rules (first part) and messages (second part)
    separated by a newline.
    """

    newline = lines.index("")
    messages = lines[newline + 1 :]

    rules = {}
    for rule in lines[:newline]:
        rule_no, remainder = rule.split(":")
        rule_no = int(rule_no)

        if "|" in remainder:
            rhs = [
                list(map(int, x.strip().split(" ")))
                for x in remainder.split("|")
            ]
        elif any([c in rule for c in ["a", "b"]]):
            rhs = remainder.strip(' "')
        else:
            rhs = [list(map(int, remainder.strip().split(" ")))]

        rules[rule_no] = rhs

    return rules, messages


def rules_to_regex(rules, index=0, loop=False, max_len=None):
    """ Build regular expression from rules. """

    # If we have the special loop (we only handle this special case)
    if loop and index == 8:
        return (
            "("
            + rules_to_regex(rules, index=42, loop=loop, max_len=max_len)
            + ")+"
        )

    if loop and index == 11:
        # This one is special, the expression will "grow" outwards from the
        # middle.
        # Consider the simple case
        #     11: "a" "b" | "a" 11 "b"
        # then 11 will be expanded to x of "a" followed by x of "b".
        exp_31 = rules_to_regex(rules, index=31, loop=loop, max_len=max_len)
        exp_42 = rules_to_regex(rules, index=42, loop=loop, max_len=max_len)

        alternatives = []
        for count in range(1, max_len // 2):
            alternatives.append(
                "{exp_42}{{{count}}}{exp_31}{{{count}}}".format(
                    exp_31=exp_31, exp_42=exp_42, count=count
                )
            )

        return "(" + "|".join(alternatives) + ")"

    rule = rules[index]

    # If we are at a character, return it
    if isinstance(rule, str):
        return rule

    alternatives = []
    for sub_rules in rule:
        alternative = ""
        for sub_rule in sub_rules:
            alternative += rules_to_regex(
                rules, sub_rule, loop=loop, max_len=max_len
            )

        alternatives.append(alternative)

    return "(" + "|".join(alternatives) + ")"


def match_messages(expression, messages):
    """ Match the messages with expression. """

    # Match a full string
    expression = "^" + expression + "$"

    count = 0
    regexp = re.compile(expression)

    for message in messages:
        if regexp.match(message):
            count += 1
    return count


if __name__ == "__main__":
    file_in = argv[1]
    with open(file_in, "r") as fh:
        lines = [line.rstrip() for line in fh.readlines()]

    rules, messages = parse_input(lines)

    exp = rules_to_regex(rules, index=0)
    count = match_messages(exp, messages)

    print("[Task 1] Count is: {}".format(count))

    max_len = max(map(len, messages))
    exp = rules_to_regex(rules, index=0, loop=True, max_len=max_len)
    count = match_messages(exp, messages)
    print("[Task 2] Count is: {}".format(count))
