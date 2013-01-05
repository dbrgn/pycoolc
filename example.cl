class Silly {
    copy() : SELF_TYPE { self };
};

-- Class sally
class Sally inherits Silly { };

-- Main function
class Main {
    x : Sally <- (new Sally).copy();

    (* main function,
       type Sally *)
    main() : Sally { x };
};
