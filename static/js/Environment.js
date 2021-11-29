class Game {
    #board;
    #level_count;
    #avatarPosition;
    #ns_positions;
    #possible_levels = [];
    #gameType;
    #action_count = [];
    #avatar_start_position;
    #ns_interactions = [];
    #wall_interactions = [];
    #maps = [];
    #self_start_locs = [];
    #self_locs = [];
    #ns_locs = []
    #current_self_locs = [];
    #current_ns_locs = [];
    #num_levels;

    constructor(gameType) {
        this.#num_levels = 5;
        this.#gameType = gameType;
        this.#level_count = 0;
        this.#avatarPosition = random_avatar_pos(gameType);
        this.#avatar_start_position = this.#avatarPosition
        this.#self_start_locs.push(JSON.parse(JSON.stringify(this.#avatar_start_position)));
        //this.#current_self_locs.push(JSON.parse(JSON.stringify(this.#avatar_start_position)));
        //console.log(this.#avatarPosition);
        this.#action_count.push(0);
        this.#ns_interactions.push(0);
        this.#wall_interactions.push(0);

        if (gameType === "logic") {
            let rn = rand(9);
            logic_levels(this.#possible_levels);
            this.#board = JSON.parse(JSON.stringify(this.#possible_levels[rn]));
        } else if (gameType === "contingency" || gameType === "change_agent") {
            contingency_levels(this.#possible_levels);
            this.#board = JSON.parse(JSON.stringify(this.#possible_levels[0]));
        }
    }

    addToMaps(oldMap) {
        this.#maps.push(JSON.parse(JSON.stringify(oldMap)));
    }

    getGameType() {
        return this.#gameType;
    }

    getNumLevels() {
        return this.#num_levels;
    }

    getBoard() {
        return this.#board;
    }

    getAvatarPos() {
        return this.#avatarPosition;
    }

    getLevelCount() {
        return this.#level_count;
    }

    getCurrentActionCount() {
        return this.#action_count[this.#level_count]
    }

    getLevels() {
        return this.#possible_levels;
    }

    getLevel(levelNo) {
        return this.#possible_levels[levelNo];
    }

    setBoard(board) {
        this.#board = board;
    }

    setAvatarPos(pos) {
        this.#avatarPosition = pos;
    }

    incrementLevelCount() {
        this.#level_count++;
    }

    increamentActionCount() {
        this.#action_count[this.#level_count]++;
    }

    nextLevel() {
        this.addToMaps(this.#board);
        if (this.#gameType === 'logic') {
            let rn = rand(9);
            this.setBoard(JSON.parse(JSON.stringify(this.getLevel(rn))));
            this.setAvatarPos(random_avatar_pos(this.#gameType));
            this.#avatar_start_position = this.#avatarPosition
            this.incrementLevelCount();
        } else if (this.#gameType === 'contingency' || this.#gameType === "change_agent") {
            this.setBoard(JSON.parse(JSON.stringify(this.getLevel(0))));
            this.setAvatarPos(random_avatar_pos(this.#gameType));
            this.#avatar_start_position = this.#avatarPosition
            this.incrementLevelCount();
        }

        this.#self_start_locs.push(JSON.parse(JSON.stringify(this.#avatar_start_position)));


        if (this.getLevelCount() === this.#num_levels) {
            //alert("Game Won!");
            //this.#self_locs.push(JSON.parse(JSON.stringify(this.#current_self_locs)))
            this.#self_locs.push(deepCopy(this.#current_self_locs));
            this.#ns_locs.push(deepCopy(this.#current_ns_locs));
            // save the data
        } else {
            this.#action_count.push(0);
            this.#wall_interactions.push(0);
            this.#ns_interactions.push(0);
            //this.#self_locs.push(JSON.parse(JSON.stringify(this.#current_self_locs)))
            this.#self_locs.push(deepCopy(this.#current_self_locs));
            this.#ns_locs.push(deepCopy(this.#current_ns_locs));
            this.#current_self_locs = [];
            this.#current_ns_locs = [];
        }
    }

    // Some of ns sprites will oscillate up and some will oscillate down
    move_ns_contingency() {
        for (let i = 0; i < 3; i++) {
            let curr = this.#ns_positions[i];
            if (curr[2] === 0) {  // horizontal move
                let rn = rand(2); // 0 = left, 1 = right
                if ((this.#ns_positions[i][1] === 17) || (this.#ns_positions[i][1] === 9)) {
                    rn = 0;
                }

                if ((this.#ns_positions[i][1] === 11) || (this.#ns_positions[i][1] === 3)) {
                    rn = 1;
                }

                if (rn === 1) { // right
                    this.#board[this.#ns_positions[i][0]][this.#ns_positions[i][1]] = 0; // old coor
                    this.#ns_positions[i] = [this.#ns_positions[i][0], this.#ns_positions[i][1] + 1, 0];
                    this.#board[this.#ns_positions[i][0]][this.#ns_positions[i][1]] = 8; // new coor
                } else if (rn === 0) { // left
                    this.#board[this.#ns_positions[i][0]][this.#ns_positions[i][1]] = 0; // old coor
                    this.#ns_positions[i] = [this.#ns_positions[i][0], this.#ns_positions[i][1] - 1, 0];
                    this.#board[this.#ns_positions[i][0]][this.#ns_positions[i][1]] = 8; // new coor
                }
            } else if (curr[2] === 1) {  // vertical move
                let rn = rand(2); // 0 = up, 1 = down

                if ((this.#ns_positions[i][0]) === 3 || (this.#ns_positions[i][0] === 11)) {
                    rn = 1;
                }

                if ((this.#ns_positions[i][0] === 9) || (this.#ns_positions[i][0] === 17)) {
                    rn = 0;
                }

                if (rn === 1) { // down
                    this.#board[this.#ns_positions[i][0]][this.#ns_positions[i][1]] = 0; // old coor
                    this.#ns_positions[i] = [this.#ns_positions[i][0] + 1, this.#ns_positions[i][1], 1];
                    this.#board[this.#ns_positions[i][0]][this.#ns_positions[i][1]] = 8; // new coor
                } else if (rn === 0) { // up
                    this.#board[this.#ns_positions[i][0]][this.#ns_positions[i][1]] = 0; // old coor
                    this.#ns_positions[i] = [this.#ns_positions[i][0] - 1, this.#ns_positions[i][1], 1];
                    this.#board[this.#ns_positions[i][0]][this.#ns_positions[i][1]] = 8; // new coor
                }

            }
        }
    }


    change_agent() {
        if (this.getCurrentActionCount() % 7 !== 0) {
            return;
        }

        let rn = rand(3); // 0, 1, 2
        let temp = this.#avatarPosition;
        this.getBoard()[temp[0]][temp[1]] = 0; // set avatar's old position to 0
        this.setAvatarPos(this.#ns_positions[rn]);
        //console.log("AGENT CHANGED. Current agent: " + this.#avatarPosition );
        this.getBoard()[this.#avatarPosition[0]][this.#avatarPosition[1]] = 8;
        this.#ns_positions[rn] = temp;
    }

    // Some of ns sprites will oscillate up and some will oscillate down
    move_ns_change_agent() {
        this.change_agent();
        let action_pos_dict = [[-1, 0], [1, 0], [0, -1], [0, 1]];
        let cc = [0] * 4;
        var rn;
        var stay = false;
        for (let i = 0; i < 3; i++) {

            do {
                rn = rand(4); // 0 = left, 1 = right, 2 = up, 3 = down

                if (cc[rn] === 0) {
                    cc[rn]++;
                } else {
                    continue;
                }

                if (cc[0] !== 0 && cc[1] !== 0 && cc[2] !== 0 && cc[3] !== 0) { // stay, cannot move anywhere
                    stay = true;
                    break;
                }

            } while (this.canMoveNs(rn, this.#ns_positions[i]) === 0); // iterate if ns cannot move

            if (!stay) {
                this.#board[this.#ns_positions[i][0]][this.#ns_positions[i][1]] = 0; // set avatar's old position to grass

                this.#ns_positions[i] = [this.#ns_positions[i][0] + action_pos_dict[rn][0],
                    this.#ns_positions[i][1] + action_pos_dict[rn][1]];

                this.#board[this.#ns_positions[i][0]][this.#ns_positions[i][1]] = 8;
            }

        }
    }

    /*
    *
    * up = 0
    * down = 1
    * left = 2
    * right = 3
    *
    */
    move(direction) {
        if (this.getGameType() === "contingency") {
            if (this.#action_count[this.#level_count] === 0) { // if it is the first action, set non self sprites
                this.contingency_ns_pos(); // set position of non-self sprites
            }

            this.move_ns_contingency(); // move non-self sprites
        } else if (this.getGameType() === "change_agent") {
            if (this.#action_count[this.#level_count] === 0) { // if it is the first action, set non self sprites
                this.contingency_ns_pos(); // set position of non-self sprites
            }

            this.move_ns_change_agent(); // move non-self sprites
        } else {
            let poss = [[1, 1], [1, 7], [7, 1], [7, 7]];

            function arraysEqual(a, b) {
                for (var i = 0; i < a.length; ++i) {
                    if (a[i] !== b[i]) return false;
                }
                return true;
            }

            const s = (a) => arraysEqual(a, this.#avatar_start_position);
            poss.splice(poss.findIndex(s), 1);
            this.#ns_positions = poss;
        }

        let x = this.getAvatarPos()[0]
        let y = this.getAvatarPos()[1]
        let new_x = x;
        let new_y = y;
        switch (direction) {
            case 0:
                new_x--;
                break;
            case 1:
                new_x++;
                break;
            case 2:
                new_y--;
                break;
            case 3:
                new_y++;
                break;
        }

        if (this.canMove(direction) === 1) {
            this.#board[x][y] = 0; // set avatar's old position to grass
            this.#board[new_x][new_y] = 8;
            this.#avatarPosition = [new_x, new_y];
            this.increamentActionCount();
            this.#current_self_locs.push(deepCopy(this.#avatarPosition));
            this.#current_ns_locs.push(deepCopy(this.#ns_positions));

        } else if (this.canMove(direction) === 2) {
            this.nextLevel();
        } else { // cannot move
            if (this.canMove(direction) === 0) { // wall
                this.#wall_interactions[this.#level_count]++;
            } else if (this.canMove(direction) === -1) { // ns
                this.#ns_interactions[this.#level_count]++;
            }

            this.#current_self_locs.push(deepCopy(this.#avatarPosition));
            this.#current_ns_locs.push(deepCopy(this.#ns_positions));
            this.increamentActionCount();
        }

        //this.#current_self_locs.push(JSON.stringify(this.#avatarPosition));


    }

    // returns 0 if the avatar cannot move to the specified location, 1 if avatar can move and 2 if avatar reaches goal
    canMove(direction) {
        let x = this.getAvatarPos()[0]
        let y = this.getAvatarPos()[1]
        var next = 0;
        switch (direction) {
            case 0: // up
                next = this.getBoard()[x - 1][y];
                break;
            case 1: // down
                next = this.getBoard()[x + 1][y];
                break;
            case 2: // left
                next = this.getBoard()[x][y - 1];
                break;
            case 3: // right
                next = this.getBoard()[x][y + 1];
                break;
        }

        if (next === 1 || next === 8) { // If there is a wall return 0. If there is ns, return -1.
            if (next === 1) {
                return 0;
            } else {
                return -1;
            }
        } else if (next === 0) { // There is grass, can move
            return 1;
        } else if (next === 3) { // Reached Goal!
            return 2;
        }
    }

    // returns 0 if the ns cannot move to the specified location, 1 if ns can move
    canMoveNs(direction, ns) {
        let x = ns[0]
        let y = ns[1]
        var next = 0;
        switch (direction) {
            case 0: // up
                next = this.getBoard()[x - 1][y];
                break;
            case 1: // down
                next = this.getBoard()[x + 1][y];
                break;
            case 2: // left
                next = this.getBoard()[x][y - 1];
                break;
            case 3: // right
                next = this.getBoard()[x][y + 1];
                break;
        }

        if (next === 1 || next === 8 || next === 3) {
            return 0;
        } else if (next === 0) { // There is grass, can move
            return 1;
        }
    }

    // Sets non-self sprite locations and directions
    // (6, 6), (14, 6), (14,14), (6, 14)
    contingency_ns_pos(direction) {
        let positions = [[6, 6], [6, 14], [14, 6], [14, 14]];

        if (this.#action_count[this.#level_count] === 0) {
            // Remove the actual self
            for (let i = 0; i < positions.length; i++) {
                if (positions[i][0] === this.#avatar_start_position[0] &&
                    positions[i][1] === this.#avatar_start_position[1]) {
                    positions.splice(i, 1);
                }
            }
        }

        let v = 2;
        let h = 2;

        // Oscillation direction is randomly assigned
        // 2 horizontal, 2 vertical
        if (direction === 0 || direction === 0) { // vertical
            v--;
        } else { // horizontal
            h--;
        }

        for (let i = 0; i < 3; i++) {
            let rn = rand(2); // 0 or 1.
            if (v === 0) {
                rn = 1;
            } else if (h === 0) {
                rn = 0;
            } else if (v === 0 && h === 0) {
                break;
            }
            // 0 = horizontal, 1 = vertical.
            positions[i].push(rn);
            if (rn === 0) {
                v--;
            } else {
                h--;
            }
        }

        this.#ns_positions = positions;
    }


    getData() {
        this.#self_start_locs.pop();
        var datamap = {
            "steps": this.#action_count,
            "game_type": this.#gameType,
            "wall_interactions": this.#wall_interactions,
            "ns_interactions": this.#ns_interactions,
            "map": this.#maps,
            "self_start_locs": this.#self_start_locs,
            "self_locs": this.#self_locs,
            "ns_locs": this.#ns_locs,
            "n_levels": this.getNumLevels()
        };

        var data = {"data": datamap}
        return data;
    }
}

// Returns random avatar position.
// (1,1), (7,1), (1,7), (7,7)
function random_avatar_pos(gameType) {
    if (gameType === "logic") {
        let positions = [[1, 1], [1, 7], [7, 1], [7, 7]];
        return positions[rand(4)];
    } else if (gameType === "contingency" || gameType === "change_agent") {
        let positions = [[6, 6], [6, 14], [14, 6], [14, 14]];
        return positions[rand(4)];
    }
}

function rand(level_amt) {
    return Math.floor(Math.random() * level_amt);
}

function logic_levels(levels) {
    levels.push([
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 8, 0, 0, 0, 0, 0, 8, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 8, 0, 0, 0, 0, 0, 8, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]);

    levels.push([
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 8, 1, 1, 0, 0, 0, 8, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 8, 0, 0, 0, 0, 0, 8, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]);

    levels.push([
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 8, 0, 0, 0, 0, 0, 8, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 8, 1, 1, 0, 0, 0, 8, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]);

    levels.push([
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 8, 0, 0, 0, 0, 0, 8, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 8, 0, 0, 0, 1, 1, 8, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]);

    levels.push([
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 8, 0, 0, 0, 1, 1, 8, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 8, 0, 0, 0, 0, 0, 8, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]);

    levels.push([
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 8, 1, 1, 0, 1, 1, 8, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 8, 1, 1, 0, 1, 1, 8, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]);

    levels.push([
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 8, 1, 1, 0, 1, 1, 8, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 8, 0, 0, 0, 1, 1, 8, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]);

    levels.push([
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 8, 1, 1, 0, 1, 1, 8, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 8, 1, 1, 0, 0, 0, 8, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]);

    levels.push([
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 8, 1, 1, 0, 0, 0, 8, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 3, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 8, 1, 1, 0, 0, 0, 8, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]);
}

function contingency_levels(levels) {
    levels.push([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]);
}

const deepCopy = (arr) => {
    let copy = [];
    arr.forEach(elem => {
        if (Array.isArray(elem)) {
            copy.push(deepCopy(elem))
        } else {
            if (typeof elem === 'object') {
                copy.push(deepCopyObject(elem))
            } else {
                copy.push(elem)
            }
        }
    })
    return copy;
}