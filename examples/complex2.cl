class Silly {
    copy() : SELF_TYPE { self };
};

-- Class sally
class Sally inherits Silly { };

-- Main function
class Main {
    x : Sally <- (new Sally).copy();
    y : Int <- 12 - 9;
    z : Int <- if y <= 42 then 5 * 3 + 2 else 0 fi;

    (* main function,
       type Sally *)
    main() : Sally { x };
};
