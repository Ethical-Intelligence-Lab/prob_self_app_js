
class Game {
    #board;
    #level_count;
    #avatarPosition;
    #possible_levels = [];
    #gameType;
    constructor( gameType ) {
        this.#gameType = gameType;
        this.#level_count = 0;
        this.#avatarPosition = random_avatar_pos(gameType);

        if( gameType === "logic") {
            let rn = rand(9);
            this.#possible_levels = logic_levels(this.#possible_levels);
            this.#board = JSON.parse(JSON.stringify(this.#possible_levels[rn]));
        } else if( gameType === "contingency") {
            // TODO
            console.log("todo");
        }
    }
}

// Returns random avatar position.
// (1,1), (7,1), (1,7), (7,7)
function random_avatar_pos(gameType) {
    if( gameType === "logic") {
        let positions = [[1,1], [1,7], [7,1], [7,7]];
        return positions[rand(4)];
    } else if( gameType === "contingency") {
        console.log("TODO");
    }
}

function rand(level_amt) {
    return Math.floor( Math.random() * level_amt );
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

/*
// Logic Game:
var levels = [];
logic_levels(levels);
var level_count = 0;


var rn = rand(9);
var board = JSON.parse(JSON.stringify(levels[rn]));

var markup = board.map(row => row.map(col => `<span class="field ${col === 8 ? "avatar" : col === 3 ? "goal" : col === 0 ? "grass" : "wall" }"></span>` ).join("")).join("<span class='clear'></span>");
document.getElementById("container").innerHTML = markup;

var avatarPosition;
random_avatar_pos();

*/