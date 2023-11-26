import React, {useCallback, useEffect, useMemo, useState} from 'react';
import './App.css';
import axios, {AxiosResponse} from "axios";
import {Button, Input, Modal, Select, Table, Typography} from "antd";
import {ColumnsType} from "antd/es/table";
import {DeleteTwoTone, FileTextOutlined, PlusCircleOutlined} from "@ant-design/icons";
import {NotesDataType, INote} from "./App.types";

function App() {
    const [notes, setNotes] = useState<Array<NotesDataType>>([]);
    const [isModalOpen, setIsOpenModal] = useState<boolean>(false);
    const [title, setTitle] = useState<string>('');
    const [description, setDescription] = useState<string>('');
    const [priority, setPriority] = useState<number>(1);

    useEffect(() => {
        axios.get('/api/notes').then((response: AxiosResponse<Array<INote>>) => {
            if (response.data) {
                const enrichedData: Array<NotesDataType> = response.data.map(({id, ...rest}) => ({...rest, key: id}));
                setNotes(enrichedData);
            }
        })
    }, []);

    const handleAddNote = useCallback(() => {
        axios.post('/api/note', {title, description, priority}, {
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        }).then((response: AxiosResponse<INote>) => {

            if (response.data.id) {
                setTitle('');
                setDescription('');
                setPriority(1);
                axios.get('/api/notes').then((response: AxiosResponse<Array<INote>>) => {
                    if (response.data) {
                        const enrichedData: Array<NotesDataType> = response.data.map(({id, ...rest}) => ({
                            ...rest,
                            key: id
                        }));
                        setNotes(enrichedData);
                    }
                })
            }
            setIsOpenModal(false);
        })
    }, [title, description, priority]);

    const handleDeleteNote = useCallback((id: number) => {
        Modal.confirm({
            title: 'Вы действительно хотите удалить заметку?',
            okText: 'Да',
            okType: 'danger',
            cancelText: 'Отменить',
            onOk: () => {
                axios.delete(`/api/note/${id}`, {
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                    }
                }).then((res) => {
                    console.log(res);
                    axios.get('/api/notes').then((response: AxiosResponse<Array<INote>>) => {
                        if (response.data) {
                            const enrichedData: Array<NotesDataType> = response.data.map(({id, ...rest}) => ({
                                ...rest,
                                key: id
                            }));
                            setNotes(enrichedData);
                        }
                    })
                })
            }
        })
    }, []);

    const columns: ColumnsType<NotesDataType> = [
        {
            title: 'id',
            dataIndex: 'id',
            key: 'id',
            render: (_, note) => {
                return <i>{note.key}</i>
            },
        },
        {
            title: 'Название заметки',
            dataIndex: 'title',
            key: 'title',
        },
        {
            title: 'Текст заметки',
            dataIndex: 'description',
            key: 'description',
        },
        {
            title: 'Приоритет',
            key: 'priority',
            dataIndex: 'priority',
        },
        {
            title: 'Дата создания',
            key: 'date_created',
            dataIndex: 'date_created',
            render: (_, note) => {
                const date = new Date(note.date_created).toUTCString();
                return <i>{date}</i>;
            },
        },
        {
            title: '',
            key: 'delete',
            dataIndex: 'delete',
            render: (_, ...rest) => {
                return <DeleteTwoTone twoToneColor="#FF4C4C" onClick={() => handleDeleteNote(rest[0].key)}/>;
            },
        },
    ];

    const createNoteBtn = useMemo(
        () => (
            <Button className='NewNote-button' onClick={() => setIsOpenModal(true)}>
                <PlusCircleOutlined/> Добавить заметку
            </Button>
        ), []);

    return (
        <div className="App">
            <header className="App-header">
                <Typography.Title level={2} color='#fff'><FileTextOutlined/> Notes App</Typography.Title>
            </header>
            {notes.length ? (
                <div className="App-body">
                    <div className='Button-wrapper'>
                        {createNoteBtn}
                    </div>
                    <Table pagination={false} columns={columns} dataSource={notes}/>
                </div>
            ) : (
                <div className="Empty-wrapper">
                    {createNoteBtn}
                </div>
            )}
            <Modal
                title="Создать новую заметку"
                open={isModalOpen}
                onOk={handleAddNote}
                okButtonProps={{
                    disabled: !title || !description
                }}
                destroyOnClose={true}
                onCancel={() => setIsOpenModal(false)}
            >
                <div>
                    <Typography.Text>Название:</Typography.Text>
                    <Input className='Modal-component' placeholder='Введите название заметки' value={title}
                           onChange={(e) => setTitle(e.target.value)}/>
                </div>
                <div>
                    <Typography.Text>Текст заметки:</Typography.Text>
                    <Input.TextArea rows={4} className='Modal-component' placeholder='Введите текст заметки'
                                    value={description}
                                    onChange={(e) => setDescription(e.target.value)}/>
                </div>
                <div>
                    <Typography.Text>Приоритет (1-5):</Typography.Text>
                    <Select
                        defaultValue={priority}
                        className='Modal-component'
                        onChange={(value) => setPriority(+value)}
                        options={[
                            {value: 1, label: 1},
                            {value: 2, label: 2},
                            {value: 3, label: 3},
                            {value: 4, label: 4},
                            {value: 5, label: 5},
                        ]}
                    />
                </div>
            </Modal>
        </div>
    );
}

export default App;
