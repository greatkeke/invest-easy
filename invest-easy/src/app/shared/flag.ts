export class Flag {
    public flag: string = "";


    constructor(ccy: string) {
        this.flag = ccy.slice(0, 2).toLocaleLowerCase();
    }
}