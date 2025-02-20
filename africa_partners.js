// Label collision detection helper
class LabelManager {
    constructor() {
        this.labels = [];
    }

    checkCollision(bbox1, bbox2) {
        return !(bbox1.x2 < bbox2.x1 || 
                bbox1.x1 > bbox2.x2 || 
                bbox1.y2 < bbox2.y1 || 
                bbox1.y1 > bbox2.y2);
    }

    findPosition(point, width, height) {
        const positions = [
            {x: 10, y: -10},  // top right
            {x: -width - 10, y: -10},  // top left
            {x: 10, y: 20},  // bottom right
            {x: -width - 10, y: 20},  // bottom left
        ];

        for (let pos of positions) {
            const bbox = {
                x1: point.x + pos.x - 2,
                y1: point.y + pos.y - 2,
                x2: point.x + pos.x + width + 2,
                y2: point.y + pos.y + height + 2
            };

            let hasCollision = false;
            for (let label of this.labels) {
                if (this.checkCollision(bbox, label)) {
                    hasCollision = true;
                    break;
                }
            }

            if (!hasCollision) {
                this.labels.push(bbox);
                return pos;
            }
        }
        return null;
    }

    clear() {
        this.labels = [];
    }
} 