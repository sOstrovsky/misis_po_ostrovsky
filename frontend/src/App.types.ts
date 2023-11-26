export interface INote {
    id: number;
    title: string;
    description: string;
    priority: number;
    date_created: string;
}

export type INewNote = Omit<INote, 'id'>;

export interface NotesDataType {
    key: number;
    title: string;
    description: string;
    priority: number;
    date_created: string;
}