import gradio as gr

def create_audio_ui(ai, storage, db, mm):
    with gr.Blocks() as demo:
        with gr.Row():
            # Show only Audio models
            model_select = gr.Dropdown(label="Select Model", choices=mm.list_models("audio"), interactive=True)
            btn_refresh = gr.Button("🔄", scale=0)
        
        with gr.Row():
            # Dropdown เลือกไฟล์เสียง
            file_select = gr.Dropdown(label="Select File", choices=storage.list_audio())
            btn_load_file = gr.Button("Load Audio", scale=0)

        with gr.Row():
            audio_player = gr.Audio(type="filepath")
            text_out = gr.Textbox(lines=3, label="Transcript")
        
        btn_run = gr.Button("Transcribe", variant="primary")
        btn_save = gr.Button("Save to DB")
        status = gr.Textbox(label="DB Status")
        
        # Logic
        def refresh_models(): return gr.Dropdown(choices=mm.list_models("audio"))
        def refresh_files(): return gr.Dropdown(choices=storage.list_audio())
        def load_audio(fname): return storage.get_path(fname)
        def save_db(fname, txt, mid): 
            db.save(fname, txt, mid)
            return "Saved!"

        btn_refresh.click(refresh_models, outputs=model_select)
        btn_load_file.click(load_audio, inputs=file_select, outputs=audio_player)
        
        btn_run.click(ai.transcribe, inputs=[audio_player, model_select], outputs=text_out)
        btn_save.click(save_db, inputs=[file_select, text_out, model_select], outputs=status)
        
        # Load initial files
        demo.load(refresh_files, outputs=file_select)
        
    return demo