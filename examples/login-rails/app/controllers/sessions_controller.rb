# frozen_string_literal: true

class SessionsController < ApplicationController
  # GET /login
  def new
    @error = params[:error].present?
  end

  # POST /login
  def create
    user = User.authenticate_by(email: params[:email], password: params[:password])
    if user
      reset_session
      session[:user_id] = user.id
      redirect_to after_sign_in_path, notice: "Signed in."
    else
      # One message for both cases. Telling someone the email exists but the
      # password is wrong confirms the account to anyone who asks.
      @error = true
      render :new, status: :unprocessable_entity
    end
  end

  private

  def after_sign_in_path
    session.delete(:return_to) || root_path
  end
end
