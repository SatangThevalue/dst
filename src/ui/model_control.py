import gradio as gr

def create_model_ui(mm):
    with gr.Blocks() as demo:
        gr.Markdown("### 🧠 Model Manager (Tag-Based)")
        with gr.Row():
            with gr.Column(variant="panel"):
                mid_input = gr.Textbox(label="Model ID", value="openai/whisper-tiny")
                tags_input = gr.CheckboxGroup(["audio", "text", "image"], label="Tags", value=["audio"])
                btn_dl = gr.Button("Download & Register", variant="primary")
                log = gr.Textbox(label="Status")
            
            with gr.Column():
                filter_tag = gr.Dropdown(["All", "audio", "text"], label="Filter", value="All")
                model_list = gr.Dropdown(label="Installed Models")
                btn_del = gr.Button("Delete", variant="stop")

        def update_list(tag):
            t = None if tag == "All" else tag
            models = mm.list_models(t)
            val = models[0] if models else None
            return gr.Dropdown(choices=models, value=val)

        # Bindings
        btn_dl.click(mm.download_model, inputs=[mid_input, tags_input], outputs=log)
        btn_dl.click(lambda: update_list("All"), outputs=model_list)
        
        filter_tag.change(update_list, inputs=filter_tag, outputs=model_list)
        
        btn_del.click(mm.delete_model, inputs=model_list, outputs=log)
        btn_del.click(lambda: update_list("All"), outputs=model_list)
        
        demo.load(lambda: update_list("All"), outputs=model_list)
    return demo