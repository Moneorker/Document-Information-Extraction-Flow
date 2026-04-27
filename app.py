import os
import shutil
import uuid
import gradio as gr

from extract_v_0_4 import process_one_file, process_folder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_ROOT = os.path.join(BASE_DIR, "output")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_ROOT, exist_ok=True)



def run_extraction(uploaded_file):
    if uploaded_file is None:
        return "请先上传 PDF 文件。", "", None

    try:
        src_path = uploaded_file if isinstance(uploaded_file, str) else uploaded_file.name

        original_name = os.path.basename(src_path)
        unique_name = f"{uuid.uuid4().hex}_{original_name}"
        saved_input_path = os.path.join(UPLOAD_DIR, unique_name)

        shutil.copy(src_path, saved_input_path)

        raw_output_file, result = process_one_file(
            saved_input_path,
            output_root=OUTPUT_ROOT
        )

        
        safe_output_path = raw_output_file

        preview_text = result["preview_text"]
        status_text = (
            f"处理完成\n"
            f"文档类型: {result['doc_type']}\n"
            f"模板: {os.path.basename(result['template_file'])}\n"
            f"下载文件: {safe_output_path}"
        )

        return status_text, preview_text, safe_output_path

    except Exception as e:
        return f"处理失败: {e}", "", None



def run_batch_extraction(uploaded_files):
    if not uploaded_files:
        return "请先上传多个 PDF 文件。", "", None

    try:
        batch_dir = os.path.join(UPLOAD_DIR, f"batch_{uuid.uuid4().hex}")
        os.makedirs(batch_dir, exist_ok=True)

        for uploaded_file in uploaded_files:
            src_path = uploaded_file if isinstance(uploaded_file, str) else uploaded_file.name
            original_name = os.path.basename(src_path)
            unique_name = f"{uuid.uuid4().hex}_{original_name}"
            saved_input_path = os.path.join(batch_dir, unique_name)
            shutil.copy(src_path, saved_input_path)

        combined_output_file, results_by_type, logs = process_folder(
            batch_dir,
            output_root=OUTPUT_ROOT
        )

        safe_output_path = combined_output_file

        ordered_doc_types = [
            "passport",
            "application_form",
            "transcript",
            "diploma_certificate",
            "english_language",
        ]

        preview_parts = []
        for doc_type in ordered_doc_types:
            if doc_type in results_by_type:
                preview_parts.append(results_by_type[doc_type]["preview_text"])

        preview_text = "\n\n".join(preview_parts) if preview_parts else "未识别到可用文件。"
        status_text = "批量处理完成\n" + "\n".join(logs)

        return status_text, preview_text, safe_output_path

    except Exception as e:
        return f"处理失败: {e}", "", None




with gr.Blocks(title="Document Extractor") as demo:
    gr.Markdown("## Document Extractor")

    with gr.Tab("单文件处理"):
        gr.Markdown("上传一个 PDF，自动匹配模板并输出结果 txt。")

        file_input = gr.File(label="上传 PDF", file_types=[".pdf"], type="filepath")
        submit_btn = gr.Button("开始抽取")

        status_box = gr.Textbox(label="状态", lines=6, interactive=False)
        preview_box = gr.Textbox(label="结果预览", lines=20, interactive=False)
        download_file = gr.File(label="下载结果 txt")

        submit_btn.click(
            fn=run_extraction,
            inputs=[file_input],
            outputs=[status_box, preview_box, download_file]
        )

    with gr.Tab("批量处理"):
        gr.Markdown("上传多个 PDF，系统会自动识别 passport / application form / transcript / diploma / english language，并汇总输出一个 txt。")

        batch_input = gr.File(
            label="上传多个 PDF",
            file_count="multiple",
            file_types=[".pdf"],
            type="filepath"
        )
        batch_btn = gr.Button("开始批量抽取")

        batch_status_box = gr.Textbox(label="状态", lines=10, interactive=False)
        batch_preview_box = gr.Textbox(label="汇总预览", lines=25, interactive=False)
        batch_download_file = gr.File(label="下载汇总 txt")

        batch_btn.click(
            fn=run_batch_extraction,
            inputs=[batch_input],
            outputs=[batch_status_box, batch_preview_box, batch_download_file]
        )

if __name__ == "__main__":
    demo.launch( server_name="0.0.0.0",
        server_port=7860,
        allowed_paths=[
            os.path.abspath(OUTPUT_ROOT),
            os.path.abspath(UPLOAD_DIR),   # 可留可不留，留着排查更方便
        ],)
